from sellathon.config.mysqlconnection import connectToMySQL
from flask import flash
from sellathon.models import product
import re	# the regex module
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# The EMAIL_REGEX object has a method called .match() that will return None if no match can be found. If the argument matches the regular expression, a match object instance is returned.

class User: 
    db = 'product_listing_schema'
    def __init__(self, data):
        self.id = data['id']
        self.fname = data['fname']
        self.lname = data['lname']
        self.email = data['email']
        self.username = data['username']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.products = []
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (fname, lname, email, username, password, created_at, updated_at)
                VALUES (%(fname)s, %(lname)s, %(email)s, %(username)s, %(password)s, NOW(), NOW() )"""
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def get_by_email(cls, email):
        query = """SELECT * FROM users
                    WHERE users.email = %(email)s;"""
        result = connectToMySQL(cls.db).query_db(query, {"email": email})
        # if no results = None 
        if not result:
            return None
        
        # instantiate object 
        return cls(result[0])
    
    @classmethod
    def validate_register(cls, data):
        is_valid = True

        if len(data['fname']) < 2:
            flash("First name must be at least 2 characters!", 'fname')
            is_valid = False
        if len(data['lname']) < 2:
            flash("Last name must be at least 2 characters!", 'lname')
            is_valid =False

              # test whether a field matches the pattern
        if not EMAIL_REGEX.match(data['email']): 
            flash("Valid email required!", 'email')
            is_valid = False
        elif cls.get_by_email(data['email']) is not None:
            flash('This email already has an account', 'email')
            is_valid = False
        
        if len(data['username']) < 3:
            flash("Username must be at least 3 characters.", 'username')
            is_valid = False

        if len(data['password']) <= 0:
            flash("Password is required", 'password')
            is_valid = False

        elif len(data['password']) < 7: 
            flash("Password must be at least 7 characters long.", 'password')
            is_valid = False

        if len(data['confirm_pass']) <= 0:
            flash("Confirm Password is required", 'confirm_pass')
            is_valid = False

        elif data['password'] != data['confirm_pass']:
            flash('Please confirm password match.', 'confirm_pass')
            is_valid = False    

        return is_valid
    
    @classmethod
    def get_by_id(cls, id):
        query = """SELECT * FROM users
                    WHERE users.id = %(id)s"""
        result = connectToMySQL(cls.db).query_db(query, {"id": id})
        return cls(result[0])
    
    @classmethod
    def get_one(cls, product_id):
        query = """SELECT * FROM products
                LEFT JOIN users ON products.user_id = users.id
                WHERE products.id = %(id)s"""   
        result = connectToMySQL(cls.db).query_db(query, {"id": product_id})
        show = cls(result[0])
        for rows_from_table in result: 
            product_data = {
                "id" : rows_from_table['id'],
                "name": rows_from_table['name'],
                "type": rows_from_table['type'],
                "category": rows_from_table['category'],
                "size": rows_from_table['size'],
                "description": rows_from_table['description'],
                "contact": rows_from_table['contact'],
                "created_at" : rows_from_table['created_at'],
                "updated_at" : rows_from_table['updated_at'],
                "user_id" : rows_from_table['user_id']
            }
            show.products.append(product.Product(product_data))
        return show
    
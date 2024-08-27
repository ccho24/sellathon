from sellathon.config.mysqlconnection import connectToMySQL
from sellathon.models import user
from flask import flash

class Product:
    db = 'product_listing_schema'
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.type = data['type']
        self.category = data['category'] 
        self.size = data['size'] 
        self.description = data['description']
        self.contact = data['contact']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None


    @classmethod
    def get_all(cls):
        query = """SELECT * FROM products
                LEFT JOIN users ON products.user_id = users.id;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_users = []
        for rows_from_table in results:
            one_product = cls(rows_from_table)
            if rows_from_table['users.id'] is not None:
                user_data = {
                "id" : rows_from_table['users.id'],
                "fname" : rows_from_table['fname'],
                "lname" : rows_from_table['lname'],
                "username" : rows_from_table['username'],
                "email" : rows_from_table['email'],
                "password" : rows_from_table['password'],
                "created_at" : rows_from_table['users.created_at'],
                "updated_at" : rows_from_table['users.updated_at']
                }

                one_product.user = (user.User(user_data))
                all_users.append(one_product)
           
        return all_users
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO products (name, type, category, size, description, contact, created_at, updated_at, user_id)
                VALUES (%(name)s, %(type)s, %(category)s, %(size)s, %(description)s, %(contact)s, NOW(), NOW(), %(user_id)s )"""

        data['category'] = data.get('category') or None
        data['size'] = data.get('size') or None
        
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def validate_save(cls,data):
        is_valid = True

        if len(data['name']) < 2:
            flash("Product name must be at least 2 characters!", 'save')
            is_valid = False
        if len(data['description']) < 5:
            flash("Description must be at least 5 characters!", 'save')
            is_valid =False
        if len(data['contact']) < 7:
            flash("Contact info must be at least 7 characters!", 'save')
            is_valid =False

        return is_valid
    
    @classmethod
    def get_by_id(cls, product_id):
        query = """SELECT * FROM products
                    WHERE products.id = %(product_id)s;"""
        result = connectToMySQL(cls.db).query_db(query, {"product_id": product_id})
 
        # instantiate object 
        return cls(result[0])
    
    @classmethod
    def edit(cls, data):
        query = """UPDATE products SET name = %(name)s, type = %(type)s, category = %(category)s,
                    size = %(size)s, description = %(description)s, contact = %(contact)s
                    WHERE id = %(product_id)s;"""
        
        data['category'] = data.get('category') or None
        data['size'] = data.get('size') or None
        
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def delete(cls, product_id):
        query = """DELETE FROM products
                    WHERE products.id = %(id)s"""
        return connectToMySQL(cls.db).query_db(query, {"id": product_id})

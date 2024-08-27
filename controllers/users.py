from flask import Flask, render_template, request, session, redirect, flash
from sellathon.models.user import User
from sellathon.models.product import Product
from sellathon import bcrypt
from sellathon import app


@app.route('/register')
def index():
    return render_template('register.html')

@app.route('/register/user', methods = ['POST'])
def register_user():
    
    if not User.validate_register(request.form):
        return redirect('/register')    
    
    user_info = User.save({
        **request.form,
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }
    )
    session['user_id'] = user_info
    print(session['user_id'])


    flash("Thank you for registering!", 'success')
    return redirect('/login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/user', methods = ['POST'])
def login_user():

    user = User.get_by_email(request.form['email'])

    if not user:
        flash("Invalid email", 'log_email')
        return redirect('/login')
    
    elif not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid password", 'log_pass')
        return redirect('/login')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user.id
    session['username'] = user.username
    print(session['user_id'])
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    all_posts = Product.get_all()
    
    if 'user_id' not in session:
        flash('You must first login.', 'secure')
        return redirect('/login')
    
    return render_template('dashboard.html', posts = all_posts )


@app.route('/logout', methods = ['POST'])
def logout():
    session.pop('user_id')
    return redirect('/login')

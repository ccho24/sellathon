from flask import Flask, render_template, redirect, request, session, flash
from sellathon.models.product import Product
from sellathon.models.user import User
from sellathon import app

@app.route('/create')
def create():
   
   if 'user_id' not in session:
    flash('You must first login.', 'secure')
    return redirect('/login')

   else:
    return render_template('create.html')

@app.route('/create/new', methods = ["POST"])
def create_post():
    if not Product.validate_save(request.form):
        return redirect('/create')

    Product.save({
        **request.form,
        'user_id' : session['user_id']      
    })
    print(session['user_id'])
    return redirect('/dashboard')

@app.route('/view/<int:product_id>')
def view(product_id):
    if 'user_id' not in session:
        flash('You must first login.', 'secure')
        return redirect('/login')

    else:
        user=User.get_one(product_id)
        return render_template('view.html', user = user)

@app.route('/edit/<int:product_id>')
def edit(product_id):
    if 'user_id' not in session:
        flash('You must first login.', 'secure')
        return redirect('/login')

    else:
        user=User.get_one(product_id)
        return render_template('edit.html', user = user)

@app.route('/edit/new', methods = ["POST"])
def edit_post():

    Product.edit({
        **request.form
    })
    return redirect('/dashboard')

@app.route('/delete/<int:product_id>')
def delete(product_id):
    if 'user_id' not in session:
        flash('You must first login.', 'secure')
        return redirect('/login')

    else:
        Product.delete(product_id)
        return redirect('/dashboard')

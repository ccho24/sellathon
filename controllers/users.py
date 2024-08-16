from flask import Flask, render_template
from sellathon import app

@app.route('/register')
def index():
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
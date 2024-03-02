from flask import Flask, render_template, redirect, abort, request, flash
from flask_session import sessions
from flask_login import login_user, logout_user, login_required
from flask_mail import Mail
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
if __name__ == "__main__":
    app.run(port=8000, debug=True)
app.secret_key = b'bhfvhsshvbdjhbs'

#landing page for app, so probably Introduction, link to login page, link to sign up page
@app.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    abort(400)
    
@app.route("/login", methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        pass
    else:
        abort(400)
    
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    elif request.method == 'POST':
        
        firstname = request.form['firstname'].strip().lower()
        surname = request.form['surname'].strip().lower()
        username = request.form['username'].strip().lower()
        email = request.form['email'].strip().lower()
        password = request.form['pwd']
        password2 = request.form['pwd2']
        usernames = getUsernames()
        emails = getEmails()
        
        if password != password2:
            error = 'Passwords must match'
            flash(error)
            return render_template('signup.html', error=error)
        elif (username, ) in usernames:
            error = 'Username already exists'
            flash(error)
            return render_template('signup.html', error=error)
        elif (email, ) in emails:
            error = 'Email already in use'
            flash(error)
            return render_template('signup.html', error=error)
        else:
            with sqlite3.connect('FoodDB.db') as con:
                cur = con.cursor()
                cur.execute("""INSERT INTO Users (FirstName,LastName,Username,Email,Password)
                            VALUES (?,?,?,?,?);""", (firstname,surname,username,email,password,))
                
            return render_template('index.html')
    else:
        abort(400)
        
def getUsernames():
    with sqlite3.connect('FoodDB.db') as con:
        cur = con.cursor()
        cur.execute("SELECT Username from Users")
        usernames =  cur.fetchall()
    return usernames

def getEmails():
    with sqlite3.connect('FoodDB.db') as con:
        cur = con.cursor()
        cur.execute("SELECT Email from Users")
        emails =  cur.fetchall()
    return emails
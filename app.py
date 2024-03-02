from flask import Flask, render_template, redirect, abort, request, session
import sqlite3

# from flask_session import sessions
# from flask_login import login_user, logout_user, login_required
# from flask_mail import Mail
# from werkzeug.utils import secure_filename
# from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)

#landing page for app, so probably Introduction, link to login page, link to sign up page
@app.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        message = 'You are not logged in'
        if 'username' in session:
            message = f'Logged in as {session["username"]}'
        return render_template('index.html', message=message)
    abort(400)

#login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    #load one page for login
    if request.method == 'GET':
        return render_template("login.html")
    #load one page for post
    elif request.method == 'POST':
        return render_template()
    #abort
    else:
        abort(400)
#Follow same pattern for methods

@app.route("/logout")
def logout():
    return redirect("/")

@app.route("/fridge", methods = ['GET'])
def fridge():
    if request.method == 'GET':
        with sqlite3.connect('FoodDB.db') as con:
            cur = con.cursor()
            items = cur.execute("SELECT Food FROM Food")
        
        return render_template("fridgehome.html", items=items)
    abort(400)


@app.route("/editfridge", methods = ['GET', 'POST'])
def editfridge():
    if request.method == 'GET':
        return render_template()
    elif request.method == 'POST':
        return render_template()
    else:
        abort(400)
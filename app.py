from flask import Flask, render_template, redirect, abort, request
from flask_session import Session
from flask_mail import Mail
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from login import login_user, logout_user, login_required

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = '192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
app.config.from_object(__name__)
Session(app)

#landing page for app, so probably Introduction, link to login page, link to sign up page
@app.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    abort(400)

#login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    #load one page for login
    if request.method == 'GET':
        return render_template("login.html")
    #load one page for post
    elif request.method == 'POST':
        with sqlite3.connect("FoodDB.db") as con:
            cur = con.cursor()
            username = request.form.get("").strip().lower()
            password = request.form.get("")
            correctpassword = cur.execute("SELECT Password FROM Users WHERE Username = ?", username)
            if check_password_hash(correctpassword, password):
                login_user(username)
                return redirect("/fridge")
            else:
                return redirect("/login")
    #abort
    else:
        abort(400)
#Follow same pattern for methods

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/fridge", methods = ['GET'])
@login_required
def fridge():
    if request.method == 'GET':
        return render_template("fridgehome.html")
    abort(400)

@app.route("/editfridge", methods = ['GET', 'POST'])
@login_required
def editfridge():
    if request.method == 'GET':
        return render_template()
    elif request.method == 'POST':
        return render_template()
    else:
        abort(400)
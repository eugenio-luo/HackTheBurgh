from flask import Flask, render_template, redirect, abort, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# from flask_session import sessions
# from flask_login import login_user, logout_user, login_required
# from flask_mail import Mail
# from werkzeug.utils import secure_filename
# from werkzeug.security import generate_password_hash, check_password_hash

con = sqlite3.connect("FoodDB.db")

app = Flask(__name__)

#landing page for app, so probably Introduction, link to login page, link to sign up page
@app.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    abort(400)

@app.route("/fridgehome", methods=['GET'])
def fridge_home():
    if request.method == 'GET':
      cur = con.cursor()
      cur.execute("SELECT Food, Quantity, ExpirationDate, PredictedExpirationDate, Photo FROM food")
      items = cur.fetchall()
      return render_template('fridgehome.html', items=items)
    abort(400)
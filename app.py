from flask import Flask, render_template, redirect
from flask_session import sessions
from flask_login import login_user, logout_user, login_required
from werkzeug import utils, security

app = Flask(__name__)

#landing page for app, so probably Introduction, link to login page, link to sign up page
@app.route("/")
def index():
    return render_template("index.html")
from flask import Flask, render_template, redirect, abort, request
from flask_session import sessions
from flask_login import login_user, logout_user, login_required
from flask_mail import Mail
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

#landing page for app, so probably Introduction, link to login page, link to sign up page
@app.route("/", methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    abort(400)
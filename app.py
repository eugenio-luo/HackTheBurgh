from flask import Flask, render_template, redirect, abort, request, flash
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
        return render_template('index.html')
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
            username = request.form.get("username").strip().lower()
            password = request.form.get("pwd")
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
        

@app.route("/fridge", methods = ['GET'])
def fridge():
    if request.method == 'GET':
        with sqlite3.connect('FoodDB.db') as con:
            cur = con.cursor()
            items = cur.execute("SELECT * FROM Food")
        
        return render_template("fridge_home.html", items=items)
    abort(400)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/addtofridge", methods = ['GET', 'POST'])
def add_to_fridge():
    if request.method == 'GET':
        return render_template('add_to_fridge.html')
    elif request.method == 'POST':
        quantity = request.form.get('quantity')
        food_name = request.form.get('food_name')
        expiration_date = request.form.get('expiration_date')

        # Check if the food item already exists
        with sqlite3.connect('FoodDB.db') as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Food WHERE Food = ?", (food_name,))
    
            cur.execute("INSERT INTO Food (Food, Quantity, ExpirationDate) VALUES (?, ?, ?)", (food_name, quantity, expiration_date))
            con.commit()
        return redirect(url_for('fridge'))  
    else:
        abort(400)

@app.route('/editfridge', methods=['POST'])
def edit_fridge():
    with sqlite3.connect('FoodDB.db') as con:
        cur = con.cursor()
        id = request.form.get('id')
        food_name = request.form.get('food_name')
        quantity = request.form.get('quantity')
        expiration_date = request.form.get('expiration_date')
        cur.execute("UPDATE Food SET Food = ?, Quantity = ?, ExpirationDate = ? WHERE Key = ?", (food_name, quantity, expiration_date, id))
        con.commit()
        return redirect('/fridge')


@app.route('/deletefridge', methods=['POST'])
def deletefridge():
    id = request.form.get('id')
    with sqlite3.connect('FoodDB.db') as con:
        cur = con.cursor()
        cur.execute("DELETE FROM Food WHERE Key = ?", (id,))

        con.commit()
    return redirect(url_for('fridge'))

# have edit form hidden under table, when edit button pressed, it unhides it, and after submit, it refreshes and hids it again
# using document.queryselector
# add event listener

    
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
                            VALUES (?,?,?,?,?);""", 
                            (firstname,surname,username,email,generate_password_hash(password, method='pbkdf2', salt_length=16),))
                
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
from flask import Flask, render_template, redirect, abort, request, sessions, url_for
import sqlite3

# from flask_session import sessions
# from flask_mail import Mail
# from werkzeug.utils import secure_filename
# from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)


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
            items = cur.execute("SELECT * FROM Food")
        
        return render_template("fridgehome.html", items=items)
    abort(400)


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
            food = cur.fetchone()
        
            if food:
                # Update the existing food item
                cur.execute("UPDATE Food SET Quantity = ?, ExpirationDate = ? WHERE Food = ?", (quantity, expiration_date, food_name))
                con.commit()
                return redirect(url_for('fridge'))
            else:
                # Add a new food item
                cur.execute("INSERT INTO Food (Food, Quantity, ExpirationDate) VALUES (?, ?, ?)", (food_name, quantity, expiration_date))
                con.commit()
        return redirect(url_for('fridge'))  
    else:
        abort(400)

@app.route('/editfridge/<Food>', methods=['GET', 'POST'])
def edit_fridge(food_name):
    with sqlite3.connect('FoodDB.db') as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Food WHERE Food = ?", (food_name,))
        food = cur.fetchone()

    if request.method == 'POST':
        quantity = request.form.get('quantity')
        expiration_date = request.form.get('expiration_date')
        cur.execute("UPDATE Food SET Quantity = ?, ExpirationDate = ? WHERE Food = ?", (quantity, expiration_date, food_name))
        con.commit()
        return redirect(url_for('fridge'))

    return render_template('add_to_fridge.html', food=food)

@app.route('/deletefridge', methods=['POST'])
def deletefridge():
    food_id = request.form.get('food_id')
    with sqlite3.connect('FoodDB.db') as con:
        cur = con.cursor()
        cur.execute("DELETE FROM Food WHERE key = ?", (food_id,))

        con.commit()
    return redirect(url_for('fridge'))
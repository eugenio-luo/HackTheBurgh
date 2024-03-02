from flask import Flask, render_template

app = Flask(__name__)

@app.route("/test")
def hello_world():
    name = 'Godfrey'
    return render_template("index.html", name = name)
from flask import session, redirect
from functools import wraps

def login_user(user):
    session['username'] = user
    return redirect("/fridge")

def logout_user(user):
    session.pop(user, None)
    return redirect("/")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get['username'] is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
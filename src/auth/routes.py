from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from src.auth.services import register_user, find_user_by_username
# create Blueprint
auth_bp = Blueprint("auth", __name__, template_folder="../templates")

@auth_bp.route('/', methods=('GET', 'POST'))
def index():
    '''INDEX ENDPOINT'''
    return render_template('index.html')

@auth_bp.route('/', methods=('GET', 'POST'))
def home():
    '''HOME ENDPOINT'''
    return render_template('home.html')

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    '''LOGIN ENDPOINT'''
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = find_user_by_username(username)
        if user and user["password"] == password:  # Check account and password
            session["user"] = {"username": user["username"], "password": user["password"]}  # Save user info in session
            return redirect(url_for("auth.profile"))
        else:
            # Report error
            flash("Invalid username or password", "error")
    return render_template("login.html")


@auth_bp.route("/register")
def register():
    '''REGISTER ENDPOINT'''
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("username")

        if find_user_by_username(username):
            flash("Registration successful. Please log in.", "error")
        else:
            register_user(username,password)
            flash("Registration successful. Please log in.", "success")
    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    '''LOGIN ENDPOINT'''
    session.clear()  # Clear all session data
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
from flask_app import app
from flask import render_template, redirect, request, session, Flask
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.idea import Idea
from flask_app.models.user import User
from flask_app.models.like import Like

from flask_bcrypt import Bcrypt
from flask import flash

bcrypt = Bcrypt(app)

############
# Default Route


@app.route("/")
def index():
    if "user_id" in session:
        return redirect("/home")
    return render_template("login_register.html")


@app.route("/register", methods=["POST"])
def register():
    if not User.validate_register(request.form):
        return redirect("/")
    hashed_pw = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashed_pw
    }
    User.register_user(data)
    user_in_db = User.get_by_email(data)
    session['user_id'] = user_in_db.id

    return redirect("/home")


@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = {
        "email": request.form["email"]
    }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/home")


@app.route("/home")
def dashboard():
    if "user_id" not in session:
        flash("Please login or register before continuing on.")
        return redirect("/")

    data = {
        "id": session["user_id"]
    }

    user_in_session = User.one_user(data)
    all_ideas = Idea.all_ideas()
    # all_likes = Idea.all_likes(data)
    return render_template("home.html", user=user_in_session, ideas=all_ideas)


@app.route("/home/alphabetic")
def dashboard_alphabetic():
    if "user_id" not in session:
        flash("Please login or register before continuing on.")
        return redirect("/")
    mysql = connectToMySQL("dance_schema")
    data = {
        "id": session["user_id"]
    }
    user_in_session = User.one_user(data)
    all_ideas = Idea.all_ideas_alphabetic()

    return render_template("home.html", user=user_in_session, ideas=all_ideas)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

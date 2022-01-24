from flask_app import app
from flask import render_template, redirect, request, session, Flask
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.idea import Idea
from flask_app.models.user import User


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
    all_friends = User.show_all_friends(data)

    return render_template("home.html", user=user_in_session, ideas=all_ideas, friends=all_friends)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/users")
def all_users():
    if "user_id" not in session:
        flash("Please login or register before continuing on.")
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    user_in_session = User.one_user(data)
    all_users = User.get_all_users()
    return render_template("all_users.html", users=all_users, user=user_in_session)


@app.route("/editprofile")
def edit_profile():
    if "user_id" not in session:
        flash("Please login or register before continuing on.")
        return redirect("/")
    data = {
        "id": session["user_id"],
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
    }
    User.edit_profile(data)
    return redirect("/home")


@app.route("/friends/<int:id>")
def all_friends(id):
    if "user_id" not in session:
        flash("Please login or register before continuing on.")
        return redirect("/")
    data = {
        "id": session["user_id"]
    }
    user_in_session = User.one_user(data)
    all_friends = User.show_all_friends(data)
    all_requests = User.show_all_requests(data)
    return render_template("friends.html", friends=all_friends, user=user_in_session, all_requests=all_requests)


@app.route("/addfriend/<int:id>")
def add_friend(id):
    data = {
        "id": id,
        "user_id": session["user_id"]
    }
    User.add_friend(data)
    return redirect(f"/friends/{id}")


@app.route("/sendrequest/<int:id>")
def send_request(id):
    data = {
        "id": id,
        "user_id": session["user_id"]
    }
    User.send_request(data)
    return redirect(f"/friends/{id}")


@app.route("/deleterequest/<int:id>")
def delete_request(id):
    data = {
        "id": id,
        "user_id": session["user_id"]
    }
    User.delete_request(data)
    return redirect(f"/friends/{id}")


@app.route("/sendmessagepage/<int:id>")
def send_message_page(id):
    data = {
        "id": session["user_id"]

    }
    data_two = {
        "id": id,
        "user_id": session["user_id"]
    }
    user_in_session = User.one_user(data)
    send_one_user = User.send_one_user(data_two)
    all_friends = User.show_all_friends(data)
    return render_template("send_message_page.html", user=user_in_session, one_user_send=send_one_user, friends=all_friends)


@app.route("/sendmessage/<int:id>", methods=["POST"])
def send_message(id):

    data_two = {
        "id": id,
        "user_id": session["user_id"],
        "content": request.form["content"]
    }

    User.sendmessage(data_two)

    return redirect("/home")


@app.route("/deletemessage/<int:id>")
def delete_message(id):

    data_two = {
        "id": id,
    }

    User.delete_message(data_two)

    return redirect("/home")


@app.route("/inbox/<int:id>")
def inbox(id):

    data = {
        "id": id,
        "user_id": session["user_id"],

    }
    all_inbox = User.inbox(data)
    all_sent = User.sent(data)
    user_in_session = User.one_user(data)

    return render_template("inbox.html", all_inbox=all_inbox, user=user_in_session, all_sent=all_sent)

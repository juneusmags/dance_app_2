from mimetypes import init
from flask_app import app
from flask import render_template, redirect, request, session, Flask, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.idea import Idea
from flask_app.models.user import User


@app.route("/create/idea")
def create_idea():
    if "user_id" not in session:
        flash("Please login or register before continuing on.")
        return redirect("/")
    return render_template("create_idea.html")


@app.route("/createidea", methods=["POST"])
def createidea():
    if not Idea.validate_idea(request.form):
        return redirect("/home")

    data = {
        "name": request.form["name"],
        "songs": request.form["songs"],
        "costume": request.form["costume"],
        "choreographers": request.form["choreographers"],
        "user_id": session["user_id"]
    }
    Idea.create_idea(data)
    return redirect("/home")


@app.route("/editidea/<int:id>", methods=["POST"])
def editidea(id):
    if not Idea.validate_idea(request.form):
        return redirect("/home")

    data = {
        "id": id,
        "name": request.form["name"],
        "songs": request.form["songs"],
        "costume": request.form["costume"],
        "choreographers": request.form["choreographers"],
    }
    Idea.editidea(data)
    return redirect("/myideas")


@app.route("/delete/<int:id>")
def delete_idea(id):
    data = {
        "id": id
    }
    Idea.deleteidea(data)
    return redirect("/home")


@app.route("/like/<int:id>", methods=["POST"])
def like_idea(id):
    data = {
        "id": id,
        "user_id": session["user_id"]
    }
    Idea.likeidea(data)
    return redirect("/home")


@app.route("/comment/<int:id>", methods=["POST"])
def comment_idea(id):
    data = {
        "id": id,
        "user_id": session["user_id"],
        "contents": request.form["content"]
    }
    if len(data["contents"]) == 0:
        flash("Please enter a comment")
    else:
        Idea.commentidea(data)
    return redirect("/home")


@app.route("/deletecomment/<int:id>")
def deletecomment(id):
    data = {
        "id": id
    }
    Idea.deletecomment(data)
    return redirect("/home")


@app.route("/myideas")
def myideas():
    if "user_id" not in session:
        flash("Please login or register before continuing on.")
        return redirect("/")

    data = {
        "id": session["user_id"]
    }
    my_ideas_user = Idea.all_my_ideas(data)
    user_in_session = User.one_user(data)

    all_friends = User.show_all_friends(data)

    return render_template("my_ideas.html", user=user_in_session, friends=all_friends, my_ideas=my_ideas_user)

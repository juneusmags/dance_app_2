from flask_app import app
from flask import render_template, redirect, request, session, Flask, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.idea import Idea


@app.route("/create/idea")
def create_idea():
    if "user_id" not in session:
        flash("Please login or register before continuing on.")
        return redirect("/")
    return render_template("create_idea.html")


@app.route("/createidea", methods=["POST"])
def createidea():
    if not Idea.validate_idea(request.form):
        return redirect("/create/idea")

    data = {
        "name": request.form["name"],
        "songs": request.form["songs"],
        "costume": request.form["costume"],
        "choreographers": request.form["choreographers"],
        "user_id": session["user_id"]
    }
    Idea.create_idea(data)
    return redirect("/home")

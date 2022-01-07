from flask_app import app
from flask import render_template, redirect, request, session, Flask
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.idea import Idea
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
from flask import flash


@app.route("/editprofile/<int:id>")
def editprofile(id):
    data = {
        "id": id
    }

    return render_template("editprofile.html")

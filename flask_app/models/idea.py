import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class Idea:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.songs = data["songs"]
        self.costume = data["costume"]
        self.choreographers = data["choreogaphers"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @staticmethod
    def validate_idea(data):
        is_valid = True
        if len(data['name']) < 1:
            flash("Please enter an idea")
            is_valid = False
        if len(data['songs']) < 1:
            flash("Please enter some songs")
            is_valid = False
        if len(data['costume']) < 1:
            flash("Please enter costume")
            is_valid = False
        if len(data['choreographers']) < 1:
            flash("Please enter some choreographers")
            is_valid = False
        return is_valid

    @classmethod
    def create_idea(cls, data):
        query = "INSERT INTO ideas (name, songs, costume, choreographers, created_at, user_id) VALUES (%(name)s, %(songs)s, %(costume)s, %(choreographers)s, NOW(), %(user_id)s)"
        return connectToMySQL('dance_schema').query_db(query, data)

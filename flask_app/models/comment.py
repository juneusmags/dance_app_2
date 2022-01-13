import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class Comment:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.songs = data["songs"]
        self.costume = data["costume"]
        self.choreographers = data["choreographers"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

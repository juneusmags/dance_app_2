import re
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


class Like:
    def __init__(self, data):
        self.id = data["id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.idea_id = data["idea_id"]
        self.user_id = data["user._id"]

    @staticmethod
    def all_likes(cls, data):
        query = "SELECT * FROM ideas JOIN likes ON ideas.id = likes.idea_id WHERE ideas.id = %(like_id)s; SELECT FOUND_ROWS();"
        likes_from_db = connectToMySQL('dance_schema').query_db(query, data)
        all_likes = []
        for like in likes_from_db:
            all_likes.append((like))
        return all_likes

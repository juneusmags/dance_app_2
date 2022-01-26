from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


EMAIL_REGEX = re.compile(r'^[a-zA-z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_register(data):
        is_valid = True
        if len(data["first_name"]) < 2:
            flash("First name must be at least 2 characters long.")
            is_valid = False
        if len(data["last_name"]) < 2:
            flash("Last name must be at least 2 characters long")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Email must be a valid email.")
            is_valid = False
        if len(data["password"]) < 5:
            flash("Password must be at least 5 characters long")
            is_valid = False
        if not (data["password"]) == data["confirm_pass"]:
            flash("Passwords must match")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_edit_profile(data):
        is_valid = True
        if len(data["first_name"]) < 2:
            flash("First name must be at least 2 characters long.")
            is_valid = False
        if len(data["last_name"]) < 2:
            flash("Last name must be at least 2 characters long")
            is_valid = False
        if not EMAIL_REGEX.match(data["email"]):
            flash("Email must be a valid email.")
            is_valid = False
        return is_valid

    @classmethod
    def register_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())"
        return connectToMySQL('dance_schema').query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("dance_schema").query_db(query, data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def one_user(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        only_user = connectToMySQL("dance_schema").query_db(query, data)
        return cls(only_user[0])

    @classmethod
    def get_all_users(cls):
        query = "SELECT * FROM users"
        users_from_db = connectToMySQL('dance_schema').query_db(query)

        all_users = []
        for user in users_from_db:
            all_users.append(user)
        return(all_users)

    @classmethod
    def show_all_friends(cls, data):
        query = "SELECT * FROM dance_schema.friends JOIN users ON friends.friend_id = users.id WHERE user_id = %(id)s;"

        friends_from_db = connectToMySQL('dance_schema').query_db(query, data)

        all_friends = []
        for friend in friends_from_db:
            all_friends.append(friend)
        return(all_friends)

    @classmethod
    def show_all_requests(cls, data):
        query = "SELECT * FROM friend_requests JOIN users ON friend_requests.user_id = users.id WHERE friend_requests.friend_id = %(id)s;"

        friends_from_db = connectToMySQL('dance_schema').query_db(query, data)

        all_friends = []
        for friend in friends_from_db:
            all_friends.append(friend)
        return(all_friends)

    @classmethod
    def add_friend(cls, data):
        query = "INSERT INTO friends (user_id, friend_id) VALUES (%(id)s, %(user_id)s);"
        query_2 = "INSERT INTO friends (user_id, friend_id, created_at, updated_at) VALUES (%(user_id)s, %(id)s, NOW(), NOW());"

        delete_request_2 = "DELETE FROM friend_requests WHERE friend_id = %(user_id)s AND user_id = %(id)s"
        query_one = connectToMySQL('dance_schema').query_db(query, data)
        query_two = connectToMySQL('dance_schema').query_db(query_2, data)

        delete_request_two = connectToMySQL(
            "dance_schema").query_db(delete_request_2, data)
        return (query_one, query_two, delete_request_two)

    @classmethod
    def delete_request(cls, data):
        delete_request_2 = "DELETE FROM friend_requests WHERE friend_id = %(user_id)s AND user_id = %(id)s"
        delete_request_two = connectToMySQL(
            "dance_schema").query_db(delete_request_2, data)
        return (delete_request_two)

    @classmethod
    def send_request(cls, data):
        query = "INSERT INTO friend_requests (user_id, friend_id, created_at, updated_at) VALUES (%(user_id)s, %(id)s, NOW(), NOW());"

        query_one = connectToMySQL('dance_schema').query_db(query, data)

        return (query_one)

    @classmethod
    def send_one_user(cls, data):
        query = "SELECT users.id, users.first_name, users.last_name, users.email, users.password, users.created_at, users.updated_at FROM friends JOIN users ON friends.user_id = users.id WHERE user_id = %(id)s;"

        only_user = connectToMySQL(
            'dance_schema').query_db(query, data)

        return cls(only_user[0])

    @classmethod
    def sendmessage(cls, data):
        query = "INSERT INTO messages (user_id, message_id, content, created_at, updated_at) VALUES (%(user_id)s, %(id)s, %(content)s, NOW(), NOW())"

        message = connectToMySQL(
            'dance_schema').query_db(query, data)

        return message

    @classmethod
    def delete_message(cls, data):
        query = "DELETE FROM dance_schema.messages WHERE id = %(id)s;"

        connectToMySQL('dance_schema').query_db(query, data)

    @classmethod
    def inbox(cls, data):
        query = "SELECT * FROM dance_schema.messages JOIN users ON user_id = users.id WHERE message_id = %(user_id)s;"

        inbox_from_db = connectToMySQL('dance_schema').query_db(query, data)

        all_inbox = []
        for inbox in inbox_from_db:
            all_inbox.append(inbox)

        return(all_inbox)

    @classmethod
    def sent(cls, data):
        query_sent = "SELECT * FROM dance_schema.messages JOIN users ON message_id = users.id WHERE user_id = %(id)s;"
        sent_from_db = connectToMySQL(
            'dance_schema').query_db(query_sent, data)
        all_sent = []
        for sent in sent_from_db:
            all_sent.append(sent)
        return(all_sent)

    @classmethod
    def edit_profile(cls, data):

        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"
        edited_profile = connectToMySQL('dance_schema').query_db(query, data)
        return edited_profile

    @classmethod
    def myprofile(cls, data):
        query = "SELECT * FROM users LEFT JOIN bio ON users.id = bio.user_id WHERE users.id = %(id)s;"
        profile_from_db = connectToMySQL('dance_schema').query_db(query, data)

        return profile_from_db[0]

    @classmethod
    def addbio(cls, data):
        query = "INSERT INTO bio (description_bio, pronoun, city, social, created_at, updated_at, user_id) VALUES (%(description_bio)s, %(pronoun)s, %(city)s, %(social)s, NOW(), NOW(), %(id)s)"
        profile_from_db = connectToMySQL('dance_schema').query_db(query, data)

        return profile_from_db

    @classmethod
    def edit_bio(cls, data):
        query = "UPDATE bio SET description_bio = %(description_bio)s, pronoun = %(pronoun)s, city = %(city)s, social = %(social)s WHERE user_id = %(id)s;"
        edited_profile = connectToMySQL('dance_schema').query_db(query, data)
        return edited_profile

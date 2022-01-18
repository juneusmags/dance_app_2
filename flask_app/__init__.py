from flask import Flask, request
from flask_app.config.mysqlconnection import connectToMySQL


app = Flask(__name__)
app.secret_key = "12345678"

global get_all_likes
get_all_likes = 10


def get_likes_count_for_idea(data):
    print(data)
    print(type(data))
    print(query)
    result = connectTquery = "SELECT * FROM likes WHERE user_id = {data}"
    oMySQL("dance_schema").query_db(query, data)
    print(result)

    likes_count = 0

    return result


# app.jinja_env.globals.update(get_all_likes=get_likes_count_for_idea(data))

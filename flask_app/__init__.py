from flask import Flask, request
from flask_app.config.mysqlconnection import connectToMySQL


app = Flask(__name__)
app.secret_key = "12345678"


def get_likes_count_for_idea(ideaID: int) -> int:

    data = {
        "idea_id": ideaID

    }
    query = "SELECT * FROM likes WHERE idea_id = %(idea_id)s"

    result = connectToMySQL("dance_schema").query_db(
        query, data)

    likes_count = len(result)

    return likes_count


app.jinja_env.globals.update(
    get_all_likes=get_likes_count_for_idea)


def get_comments(ideaIDs: int) -> int:
    data = {
        "idea_ids": ideaIDs
    }

    query = "SELECT content, comments.created_at, users.first_name FROM comments JOIN users ON comments.user_id = users.id WHERE comments.idea_id = %(idea_ids)s"

    result = connectToMySQL("dance_schema").query_db(query, data)
    all_comments = []
    # for index in range(len(result)):
    #     for key in result[index]:
    #         all_comments.append((result[index][key]))
    for comment in result:
        all_comments.append((comment))
    return all_comments


app.jinja_env.globals.update(
    get_all_comments=get_comments)

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

#####################################################################


def get_comments_count_for_idea(ideaID: int) -> int:

    data = {
        "idea_id": ideaID

    }
    query = "SELECT * FROM comments WHERE idea_id = %(idea_id)s"

    result = connectToMySQL("dance_schema").query_db(
        query, data)

    comments_count = len(result)

    return comments_count


app.jinja_env.globals.update(
    get_all_comments_count=get_comments_count_for_idea)
####################################################################


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


####################################################################


def validate_friend(login_user: int, friend_user: int) -> int:
    data = {
        "login_user": login_user,
        "friend_user": friend_user
    }

    query = "SELECT * FROM friends JOIN users ON friends.user_id = users.id WHERE users.id = %(login_user)s AND friends.friend_id = %(friend_user)s;"
    result = connectToMySQL("dance_schema").query_db(query, data)
    if len(result) == 0:
        result = True
    return result


app.jinja_env.globals.update(
    validate_friend=validate_friend)

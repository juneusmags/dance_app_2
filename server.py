from flask_app import app
from flask_app.controllers import users, ideas

from flask import flash


if __name__ == "__main__":
    app.run(debug=True)

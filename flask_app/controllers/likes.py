from flask_app import app
from flask import render_template, redirect, request, session, Flask, flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.idea import Idea
from flask_app.models.like import Like

from flask import Blueprint, render_template

api = Blueprint('api', __name__)

from . import authentication, comments, errors, posts, users
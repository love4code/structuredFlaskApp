from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
# This blueprint neds to be attached to the application in the
# create_app() factory function (app package constructor)
from flask import Flask, render_template
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager = LoginManager()
# Keep Track of users IP address and browser agent and log out if change
# is detected
login_manager.session_protection = 'strong'
# Set end point to 'auth/login, because route is in the blueprint it
# needs to be prefixed with the blueprint name
login_manager.login_view = 'auth.login'

# create a factory Function to create our application
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # Define routes and custom error pages here
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    # The url_prefix() argument is optional. When used, all the routes
    # defined in the blueprint will be registered with the given prefix,
    # in this case /auth
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
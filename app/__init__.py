# yourapp/__init__.py
import os
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash
import logging

mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'login'  
migrate = Migrate()


def create_app(config_filename='config.py'):
    app = Flask(__name__)

    # Load the default configuration
    app.config.from_object('config.default')
    # Load the instance configuration, if it exists, when not testing
    app.config.from_pyfile(config_filename, silent=True)

    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Import and register blueprints
    from .blueprints.AHB import AHB as ahb_bp
    app.register_blueprint(ahb_bp)


    # blueprint for auth routes in our app
    from .blueprints.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')


    return app


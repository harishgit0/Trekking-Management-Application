from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from application.config import Config
from application.database import db
from application.cache import cache

jwt = JWTManager()
mail = Mail()


def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    CORS(app)

    db.init_app(app)
    cache.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    return app
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from application.config import Config
from application.database import db
from application.cache import cache

jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # ✅ LOAD CONFIG PROPERLY
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    cache.init_app(app)
    jwt.init_app(app)

    return app
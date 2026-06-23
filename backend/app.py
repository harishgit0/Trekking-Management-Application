from flask import Flask, request, jsonify
from application.config import Config
from application.database import db
from application.models import *

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)





with app.app_context():
    db.create_all()
    admin = User.query.filter_by(role="admin").first()

    if not admin:
        admin = User(
            username="admin",
            email="admin@trek.com",
            password="admin123",   # hash later
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)
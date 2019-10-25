import os
import sys
from flask import Flask
from config import Config
from routes import blue
from database import db
from loginman import login_initializing

sys.path.append(os.path.dirname(__name__))


def create_app():
    app = Flask(__name__)
    # Getting configuration info from config.py
    app.config.from_object(Config)
    db.init_app(app)
    login_initializing(app)
    app.register_blueprint(blue, url_prefix='')

    return app


def create_database(app):
    from models import User
    db.create_all(app)


if __name__ == '__main__':
    app = create_app()
    create_database(app)
    app.run()
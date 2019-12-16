import os
import sys
from flask import Flask
from config import Config
from routes import blue
from database import db
from loginman import login_initializing
from models import User

sys.path.append(os.path.dirname(__name__))


def create_app():
    app = Flask(__name__)
    # Getting configuration info from config.py
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        try:
            master_password = open("/run/secrets/master_password", "r").read().strip()
            master_phone = open("/run/secrets/master_phone", "r").read().strip()
            admin = User(username='admin', phone=master_phone)
            admin.set_password(master_password, master_phone)
            db.session.add(admin)
            db.session.commit()
        except Exception:
            pass
    login_initializing(app)
    app.register_blueprint(blue, url_prefix='')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()

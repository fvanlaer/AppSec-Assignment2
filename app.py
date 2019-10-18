import os
import sys
from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

sys.path.append(os.path.dirname(__name__))

app = Flask(__name__)
# Getting configuration info from config.py
app.config.from_object(Config)

login = LoginManager(app)

# Database
db =  SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
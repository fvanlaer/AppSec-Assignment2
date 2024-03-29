import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    try:
        SECRET_KEY = open("/run/secrets/SECRET_KEY", "r").read().strip()
    except Exception:
        SECRET_KEY = 'donotknow'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

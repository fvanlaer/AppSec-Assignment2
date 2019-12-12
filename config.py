import os
from get_docker_secret import get_docker_secret
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SECRET_KEY = get_docker_secret('SECRET_KEY', default='donotknow')

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

from flask_login import LoginManager

login = LoginManager()


def login_initializing(app):

    login = LoginManager(app)
    login.login_view = 'login'

from flask_login import LoginManager

login = LoginManager()


def login_initializing(app):

    login.init_app(app)
    login.login_view = 'login'

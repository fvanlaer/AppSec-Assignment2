import pytest
import os
import app
import subprocess
from models import User
from database import db


@pytest.fixture()
def my_app():
    my_app = app.create_app()
    my_app.debug = True
    my_app.config['WTF_CSRF_ENABLED'] = False

    my_client = my_app.test_client()

    ctx = my_app.app_context()
    ctx.push()

    yield my_client

    ctx.pop()


@pytest.fixture()
def init_db():
    db.create_all()

    admin = User(username='BOSS', phone='9876543210')
    admin.set_password('masterandcommander', '9876543210')

    db.session.add(admin)
    db.session.commit()

    yield db

    db.drop_all()


def test_initial_page_status(my_app):
    index_page = my_app.get("/")
    login_page = my_app.get("/login")
    register_page = my_app.get("/register")
    spellcheck_page = my_app.get("/spell_check")

    # Index page redirects to login page --> code = 302 (redirect)
    assert index_page.status_code == 302
    # Login should be accessible to anybody --> code = 200
    assert login_page.status_code == 200
    # Register should be accessible to anybody --> code = 200
    assert register_page.status_code == 200
    # Spellcheck should NOT be accessible to unlogged users --> code = 302 (redirect)
    assert spellcheck_page.status_code == 302


def test_password_hash():
    # Creating new user
    current_user = User(username='francois')
    # Setting his password and phone number
    current_user.set_password('applicationsecurity', '2129981212')
    # If password is wrong but phone number is right
    assert current_user.check_password('mobilesecurity', '2129981212') == False
    # If password is right but phone number is wrong
    assert current_user.check_password('applicationsecurity', '1234567890') == False
    # If both are right
    assert current_user.check_password('applicationsecurity', '2129981212') == True


def test_register(my_app, init_db):
    username = "subordinate"
    password = "helloworld"
    phone = "1234567890"
    attempt = my_app.post("/register", data=dict(username=username, password=password, phone=phone), follow_redirects=False)
    assert b'Success' in attempt.data
    assert attempt.status_code == 200


# def login(launch_app, username, password, phone):
#     return launch_app.post("/login", data={"username": username, "password": password, "phone": phone})
#
#
# def logout(launch_app):
#     return launch_app.get('/logout')
#
#
# def test_register(launch_app):
#     attempt = launch_app.post("/register", data=dict(username="test", password="test", phone="1234567890"))
#     print(attempt.data)
#
#
# def test_login_logout(launch_app):
#     login_attempt = login(launch_app, "test", "test", "1234567890")
#     print(login_attempt.data)
#     assert login_attempt.status_code == 200
#     spellcheck_attempt = launch_app.get("/spell_check")
#     assert spellcheck_attempt.status_code == 200
#     logout_attempt = logout(launch_app)
#     assert logout_attempt.status_code == 302
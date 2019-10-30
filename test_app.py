import pytest
import app
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
    # Creation of a new user
    username1 = "student"
    password1 = "helloworld"
    phone1 = "1234567890"
    # We register our new user.
    attempt1 = my_app.post("/register", data=dict(username=username1, password=password1, phone=phone1), follow_redirects=False)
    # "Success" should be printed on the page if registration was a success.
    assert b'Success' in attempt1.data
    # Verifying there are no other errors
    assert attempt1.status_code == 200

    # Creation of another user
    username2 = "BOSS"
    password2 = "trying-hard"
    phone2 = "5552120000"
    # This registration should fail given that the username is already used.
    attempt2 = my_app.post("/register", data=dict(username=username2, password=password2, phone=phone2), follow_redirects=False)
    assert b'Failure' in attempt2.data
    # Verifying there are no other errors
    assert attempt2.status_code == 200


def test_login_logout(my_app, init_db):
    # Using the same credentials created in init_db
    username = "BOSS"
    password = "masterandcommander"
    phone = "9876543210"
    # We login.
    attempt = my_app.post("/login", data=dict(username=username, password=password, phone=phone), follow_redirects=False)
    # "Success" should be printed on the page if login was a success.
    assert b'Success' in attempt.data
    # Verifying there are no other errors
    assert attempt.status_code == 200

    # We should have access to spell_check now.
    attempt = my_app.get("/spell_check")
    # Previously, status_code was 302. It should be 200 now.
    assert attempt.status_code == 200

    # Time to log out
    attempt = my_app.get("/logout")
    attempt = my_app.get("spell_check")
    # Now that we are logged out, status_code should be back to 302
    assert attempt.status_code == 302


def test_full_spellcheck(my_app, init_db):
    # Using the same credentials created in init_db
    username = "BOSS"
    password = "masterandcommander"
    phone = "9876543210"

    # We have to log in in order to use the spell checker.
    attempt = my_app.post("/login", data=dict(username=username, password=password, phone=phone), follow_redirects=False)
    # "Success" should be printed on the page if login was a success.
    assert b'Success' in attempt.data
    # Verifying there are no other errors
    assert attempt.status_code == 200

    text_to_check = "Take a sad sogn and make it better. Remember to let her under your skyn, then you begin to make it betta."

    # Now that we are logged in, we can use the spell checker. We submit our text.
    attempt = my_app.post("/spell_check", data=dict(text_to_check=text_to_check), follow_redirects=False)
    # Verifying that the spell checker ran normally.
    assert b'sogn, skyn, betta' in attempt.data
    # Verifying there are no other errors
    assert attempt.status_code == 200

    # Time to log out
    attempt = my_app.get("/logout")
    attempt = my_app.get("spell_check")
    # Now that we are logged out, status_code should be back to 302
    assert attempt.status_code == 302

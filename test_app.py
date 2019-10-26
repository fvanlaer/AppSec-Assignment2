import pytest
import os
import app
from models import User
import unittest
from flask import Flask
from database import db
from config import Config

# @pytest.fixture()
# def my_app():
#     my_app = app.create_app()
#     my_app.debug = True
#     return my_app.test_client()
#
#
# def test_initial_page_status(my_app):
#     index_page = my_app.get("/")
#     login_page = my_app.get("/login")
#     register_page = my_app.get("/register")
#     spellcheck_page = my_app.get("/spell_check")
#
#     # Index page redirects to login page --> code = 302 (redirect)
#     assert index_page.status_code == 302
#     # Login should be accessible to anybody --> code = 200
#     assert login_page.status_code == 200
#     # Register should be accessible to anybody --> code = 200
#     assert register_page.status_code == 200
#     # Spellcheck should NOT be accessible to unlogged users --> code = 302 (redirect)
#     assert spellcheck_page.status_code == 302
#
#
# def test_password_hash():
#     # Creating new user
#     current_user = User(username='francois')
#     # Setting his password and phone number
#     current_user.set_password('applicationsecurity', '2129981212')
#     # If password is wrong but phone number is right
#     assert current_user.check_password('mobilesecurity', '2129981212') == False
#     # If password is right but phone number is wrong
#     assert current_user.check_password('applicationsecurity', '1234567890') == False
#     # If both are right
#     assert current_user.check_password('applicationsecurity', '2129981212') == True
#
#
# def test_unique_username():
#     current_user = User(username='jethro')
#     app.db.session.add(current_user)
#
#

# def register(my_app, username, password, phone):
#     return my_app.post("/register", data={"username": username, "password": password, "phone": phone})


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


class MyAppTestCases(unittest.TestCase):

    def setUp(self):
        my_app = app.create_app()
        self.my_app = my_app.test_client()

    def test_initial_status(self):
        index_page = self.my_app.get("/")
        login_page = self.my_app.get("/login")
        register_page = self.my_app.get("/register")
        spellcheck_page = self.my_app.get("/spell_check")
        self.assertEqual(index_page.status_code, 302)
        self.assertEqual(login_page.status_code, 200)
        self.assertEqual(register_page.status_code, 200)
        self.assertEqual(spellcheck_page.status_code, 302)

    def test_password_hash(self):
        # Creating new user
        current_user = User(username='francois')
        # Setting his password and phone number
        current_user.set_password('applicationsecurity', '2129981212')
        # If password is wrong but phone number is right
        self.assertFalse(current_user.check_password('mobilesecurity', '2129981212'))
        # If password is right but phone number is wrong
        self.assertFalse(current_user.check_password('applicationsecurity', '1234567890'))
        # If both are right
        self.assertTrue(current_user.check_password('applicationsecurity', '2129981212'))

    def test_unique_username(self):
        current_user = User(username='jethro')
        second_user = User(username='jethro')
        third_user = User(username='ducky')
        app_test = Flask(__name__)
        app_test.config.from_object(Config)
        db.init_app(app_test)
        with app_test.app_context():
            db.create_all()
            db.session.add(current_user)
            db.session.commit()
            self.assertTrue(User.query.filter_by(username=second_user.username).first())
            self.assertFalse(User.query.filter_by(username=third_user.username).first())
            db.drop_all()

    def test_binary_output(self):



if __name__ == '__main__':
    unittest.main()

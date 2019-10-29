import os
import app
import subprocess
from models import User
import unittest
from flask import Flask
from database import db
from config import Config


class MyAppTestCases(unittest.TestCase):

    def setUp(self):
        my_app = app.create_app()
        self.my_app = my_app.test_client()

    def test_initial_status(self):
        index_page = self.my_app.get("/")
        login_page = self.my_app.get("/login")
        register_page = self.my_app.get("/register")
        spellcheck_page = self.my_app.get("/spell_check")
        # Index page redirects to login page --> code = 302 (redirect)
        self.assertEqual(index_page.status_code, 302)
        # Login should be accessible to anybody --> code = 200
        self.assertEqual(login_page.status_code, 200)
        # Register should be accessible to anybody --> code = 200
        self.assertEqual(register_page.status_code, 200)
        # Spellcheck should NOT be accessible to unlogged users --> code = 302 (redirect)
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
            # Returns True given that second_user.username == current_user.username
            self.assertTrue(User.query.filter_by(username=second_user.username).first())
            # Returns False given that third_user.username != current_user.username
            self.assertFalse(User.query.filter_by(username=third_user.username).first())
            db.drop_all()
        os.remove("app.db")

    def test_spellcheck_output(self):
        command = ["./spell_check", "test1.txt", "wordlist.txt"]
        sub = subprocess.Popen(command, stdout=subprocess.PIPE)
        misspelled = sub.communicate()[0].decode("utf-8").replace("\n", ", ")[:-2]
        self.assertEqual(misspelled, "sogn, skyn, betta")


if __name__ == '__main__':
    unittest.main()

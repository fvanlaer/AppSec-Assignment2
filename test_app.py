import pytest
import app
import unittest


@pytest.fixture()
def launch_app():
    my_app = app.create_app()
    testing_client = my_app.test_client()
    ctx = my_app.app_context()
    ctx.push()
    yield testing_client
    ctx.pop()


def test_initial_status(launch_app):
    index_page = launch_app.get("/")
    login_page = launch_app.get("/login")
    register_page = launch_app.get("/register")
    spellcheck_page = launch_app.get("/spell_check")

    # Index page redirects to login page --> code = 302 (redirect)
    assert index_page.status_code == 302
    # Login should be accessible to anybody --> code = 200
    assert login_page.status_code == 200
    # Register should be accessible to anybody --> code = 200
    assert register_page.status_code == 200
    # Spellcheck should NOT be accessible to unlogged users --> code = 302 (redirect)
    assert spellcheck_page.status_code == 302


# def register(my_app, username, password, phone):
#     return my_app.post("/register", data={"username": username, "password": password, "phone": phone})


def login(launch_app, username, password, phone):
    return launch_app.post("/login", data={"username": username, "password": password, "phone": phone})


def logout(launch_app):
    return launch_app.get('/logout')


def test_register(launch_app):
    attempt = launch_app.post("/register", data=dict(username="test", password="test", phone="1234567890"))
    print(attempt.data)


def test_login_logout(launch_app):
    login_attempt = login(launch_app, "test", "test", "1234567890")
    print(login_attempt.data)
    assert login_attempt.status_code == 200
    spellcheck_attempt = launch_app.get("/spell_check")
    assert spellcheck_attempt.status_code == 200
    logout_attempt = logout(launch_app)
    assert logout_attempt.status_code == 302


# class MyAppTestCases(unittest.TestCase):
#
#     def setUp(self):
#         my_app = app.create_app()
#         self.my_app = my_app.test_client()
#
#     def test_initial_status(self):
#         index_page = self.my_app.get("/")
#         login_page = self.my_app.get("/login")
#         register_page = self.my_app.get("/register")
#         spellcheck_page = self.my_app.get("/spell_check")
#         self.assertEqual(index_page.status_code, 302)
#         self.assertEqual(login_page.status_code, 200)
#         self.assertEqual(register_page.status_code, 200)
#         self.assertEqual(spellcheck_page.status_code, 302)
#
#     def test_register(self):
#         attempt = self.my_app.post('/register', data=dict(username='test', password='test', phone='1234567890'))
#         self.assertIn(b'id', attempt.data)
#         login_attempt = self.my_app.post('/login', data=dict(username='test', password='test', phone='1234567890'))
#         self.assertIn(b'Success', login_attempt.data)
#         spellcheck_access = self.my_app.get("/spell_check")
#         self.assertEqual(spellcheck_access.status_code, 200)
#
#
# if __name__ == '__main__':
#     unittest.main()

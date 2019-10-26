import pytest
import app


@pytest.fixture()
def my_app():
    my_app = app.create_app()
    return my_app.test_client()


def test_initial_status(my_app):
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


def login(my_app, username, password):
    return my_app.post("/login", data=dict(username=username, password=password))
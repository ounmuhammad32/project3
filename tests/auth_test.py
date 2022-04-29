"""This test authorization pages"""
from app.db.models import User
from app import db
from tests.user_fixture import add_db_user_fixture, TEST_EMAIL, TEST_PASSWORD # pylint: disable=unused-import


def test_request_main_menu_links(client):
    """This makes the index page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'href="/login"' in response.data
    assert b'href="/register"' in response.data

def test_auth_pages(client):
    """This makes the index page"""
    response = client.get("/dashboard")
    assert response.status_code == 302
    response = client.get("/register")
    assert response.status_code == 200
    response = client.get("/login")
    assert response.status_code == 200


def test_register(client):
    """ POST to /register """
    new_email = 'newuser@test.test'
    new_password = 'Test1234!'
    assert not User.query.filter_by(email=new_email).first()

    data = {
        'email' : new_email,
        'password' : new_password,
        'confirm' : new_password
    }
    resp = client.post('register', data=data)

    assert resp.status_code == 302

    # verify new user is in database
    new_user = User.query.filter_by(email=new_email).first()
    assert new_user.email == new_email

    db.session.delete(new_user) # pylint: disable=no-member


def test_login(client, add_db_user_fixture):
    """ POST to login """
    # pylint: disable=unused-argument,redefined-outer-name

    data = {
        'email' : TEST_EMAIL,
        'password' : TEST_PASSWORD
    }
    resp = client.post('login', follow_redirects=True,
            data=data)

    # if login, redirect to /dashboard
    assert resp.status_code == 200
    assert b'<h2>Dashboard</h2>' in resp.data


def test_dashboard(application, add_db_user_fixture):
    """ GET to dashboard as logged in user """
    # pylint: disable=redefined-outer-name
    user = add_db_user_fixture

    with application.test_client(user=user) as client:
        resp = client.get('dashboard')

    # check if successful at getting /dashboard
    assert resp.status_code == 200
    assert b'<h2>Dashboard</h2>' in resp.data
    assert b'<p>Welcome: testuser@test.com</p>' in resp.data
    assert b'<h2>Browse: Your Songs</h2>' in resp.data


def test_dashboard_unauthorized(client):
    """ GET to /dashboard as unauthorized user """

    resp = client.get('dashboard', follow_redirects=True)

    # should be redirected to login page
    assert resp.status_code == 200
    assert b'<h2>Login</h2>' in resp.data
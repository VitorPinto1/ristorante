from unittest.mock import patch, MagicMock
from test.conftest import *


def test_homepage_renders(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Ristorante" in response.data
    assert b'Ristorante "Il Capo"' in response.data
    assert b'Ristorante Il Capo' in response.data
    assert b'id="menu-section"' in response.data

# LOGIN


def test_login_success_user(client):
    response = client.post('/login/login', data={
        'name': 'testuser',
        'password': 'Testuser1#'
    }, follow_redirects=False)  
    assert response.status_code == 302
    assert '/user' in response.location  

def test_login_user_not_exist(client):
    response = client.post('/login/login', data={
        'name': 'noexist',
        'password': 'Fakepassword1#'
    }, follow_redirects=True)
    assert response.status_code == 401
    assert "Invalid name or password" in response.get_data(as_text=True)

def test_session_creation_on_login(client):
    with client:
        client.post('/login/login', data={
            'name': 'testuser',
            'password': 'Testuser1#'
        }, follow_redirects=True)
        assert 'user_id' in session

def test_login_with_empty_data(client):
    response = client.post('/login/login', data={
        'name': '',
        'password': ''
    }, follow_redirects=True)
    assert response.status_code == 401
    assert "All fields are required!" in response.get_data(as_text=True)


# SIGN UP


def test_sign_up_missing_name(client):
    response = client.post('/sign_up/sign_up', data={
        'name': '',
        'email': 'newuser@example.com',
        'password': 'Password1!'
    }, follow_redirects=True)    
    assert response.status_code == 401
    assert "All fields are required!" in response.get_data(as_text=True)

def test_sign_up_missing_email(client):
    response = client.post('/sign_up/sign_up', data={
        'name': 'newuser',
        'email': '',
        'password': 'Password1!'
    }, follow_redirects=True)
    assert response.status_code == 401
    assert "All fields are required!" in response.get_data(as_text=True)

def test_sign_up_missing_password(client):
    response = client.post('/sign_up/sign_up', data={
        'name': 'newuser',
        'email': 'newuser@example.com',
        'password': ''
    }, follow_redirects=True)
    assert response.status_code == 401
    assert "All fields are required!" in response.get_data(as_text=True)
    
def test_sign_up_existing_email(client):
    response = client.post('/sign_up/sign_up', data={
        'name': 'testuserB',
        'email': 'testuser@hotmail.com',
        'password': 'Password12#'
    }, follow_redirects=True)
    assert response.status_code == 401
    assert "Email address already exists" in response.get_data(as_text=True)

def test_sign_up_existing_username(client):
    response = client.post('/sign_up/sign_up', data={
        'name': 'testuser',
        'email': 'testuser5@hotmail.com',
        'password': 'Testuser5#'
    }, follow_redirects=True)
    assert response.status_code == 401
    assert "Username already exists" in response.get_data(as_text=True)

def test_sign_up_success(client):
    response = client.post('/sign_up/sign_up', data={
        'name': 'newuser',
        'email': 'newuser@example.com',
        'password': 'Password123!'
    }, follow_redirects=False)
    assert response.status_code == 302
    follow_response = client.get(response.location, follow_redirects=True)
    assert follow_response.status_code == 200
    assert b'Index' in follow_response.data  


# RESERVATION


def test_reservation_success(client):
    with client:
        client.post('/login/login', data=dict(
            name='testuser',
            password='Testuser1#'
        ), follow_redirects=True)
        response = client.post('/reservation/reservation', data=dict(
            name='Test User',
            totalPerson=4,
            date='2024-07-29',
            time='19:00',
            email='testuser@example.com'
        ), follow_redirects=False)
        assert response.status_code == 302
        location = response.location if isinstance(response.location, str) else response.location.decode('utf-8')
        confirmation_response = client.get(location, follow_redirects=True)
        assert confirmation_response.status_code == 200
        assert b'Hello Test User, your reservation number' in confirmation_response.data
 
def test_reservation_missing_fields(client):
    with client:
        response = client.post('/login/login', data=dict(
            name='testuser',
            password='Testuser1#'
        ), follow_redirects=True)
        response = client.post('/reservation/reservation', data=dict(
            name='',
            totalPerson=4,
            date='2024-07-28',
            time='19:00',
            email=''
        ), follow_redirects=True)
        assert response.status_code == 401
        assert 'Reservation' in response.get_data(as_text=True)

def test_reservation_exceed_limit(client):
    with client:
        response = client.post('/login/login', data=dict(
            name='testuser',
            password='Testuser1#'
        ), follow_redirects=True)
        response = client.post('/reservation/reservation', data=dict(
            name='Test User',
            totalPerson=15,
            date='2024-07-28',
            time='19:00',
            email='testuser@example.com'
        ), follow_redirects=True)
        assert response.status_code == 401
        assert 'Reservation' in response.get_data(as_text=True)

def test_reservation_confirmation_email(client, mail):
    with client:
        client.post('/login/login', data=dict(
            name='testuser',
            password='Testuser1#'
        ), follow_redirects=True)
        with mail.record_messages() as outbox:
            response = client.post('/reservation/reservation', data=dict(
                name='Test User',
                totalPerson=4,
                date='2024-07-30',
                time='19:00',
                email='testuser@hotmail.com'
            ), follow_redirects=False)
            assert response.status_code == 302
            confirmation_response = client.get(response.location, follow_redirects=True)
            assert confirmation_response.status_code == 200
            assert 'Hello Test User, your reservation number' in confirmation_response.get_data(as_text=True)
            assert len(outbox) == 1
            assert outbox[0].subject == 'Reservation Confirmation'
            assert 'Hello Test User' in outbox[0].body
            assert 'Your reservation number' in outbox[0].body
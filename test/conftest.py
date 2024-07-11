import pytest
from flask import Flask, g, session
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import MySQLdb
from dotenv import load_dotenv
import os
import sys
from itsdangerous import URLSafeTimedSerializer

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app

os.environ['FLASK_ENV'] = 'test'

load_dotenv('.env.test')

@pytest.fixture(scope='module')
def app():
    flask_app.config['TESTING'] = True
    flask_app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    flask_app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    flask_app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    flask_app.config['MYSQL_DB'] = os.getenv('MYSQL_DATABASE')
    flask_app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT'))
    flask_app.config['SERVER_NAME'] = 'localhost:5000'
    flask_app.config['WTF_CSRF_ENABLED'] = False
    flask_app.config['MAIL_SUPPRESS_SEND'] = False
    mysql = MySQL(flask_app)  
    bcrypt = Bcrypt(flask_app)
    mail = Mail(flask_app)
    ts = URLSafeTimedSerializer(flask_app.config['SECRET_KEY'])
    flask_app.ts = ts
    
    try:
        with flask_app.app_context():
            yield flask_app
    except Exception as e:
        print(f"Error during app fixture setup: {e}")
    finally:
        try:
            if hasattr(mysql, 'connection') and mysql.connection.open:
                mysql.connection.close()
        except Exception as e:
            print(f"Error during MySQL connection close: {e}")

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def authenticated_client(client):
    test_user = {
        'name': 'testuser',
        'password': 'Testuser1#'
    }
    with client:
        client.post('/login/', data={
            'name': test_user['name'],
            'password': test_user['password']
        })
        yield client

@pytest.fixture
def mail(app):
    app.config['MAIL_SUPPRESS_SEND'] = False
    mail = Mail(app)
    yield mail

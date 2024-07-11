from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, make_response
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash
from flask_bootstrap import Bootstrap
from datetime import datetime, time as dt_time
from dotenv import load_dotenv
from flask_mail import Mail, Message
import os
import logging
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

env = os.getenv('FLASK_ENV', 'development')

dotenv_path = f'.env.{env}'
load_dotenv(dotenv_path)

print(f"Current environment: {env}")
print(f"MYSQL_USER: {os.getenv('MYSQL_USER')}")
print(f"MYSQL_PASSWORD: {os.getenv('MYSQL_PASSWORD')}")
print(f"MYSQL_DB: {os.getenv('MYSQL_DATABASE')}")
print(f"MYSQL_HOST: {os.getenv('MYSQL_HOST')}")
print(f"MYSQL_PORT: {os.getenv('MYSQL_PORT')}")
print(f"APP_SECRETKEY: {os.getenv('APP_SECRETKEY')}")


app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRETKEY')

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT'))
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DATABASE')

mysql = MySQL(app)
bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)


app.config['MAIL_DEFAULT_SENDER'] = 'staniaprojets@gmail.com'
app.config['MAIL_SERVER']='localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

ts = URLSafeTimedSerializer(app.secret_key)

logging.basicConfig(level=logging.INFO)





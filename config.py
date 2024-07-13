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

app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['MAIL_SERVER']= os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] =os.environ.get('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'false').strip().lower() in ['true', '1', 't']
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'false').strip().lower() in ['true', '1', 't']

mail = Mail(app)

ts = URLSafeTimedSerializer(app.secret_key)

logging.basicConfig(level=logging.INFO)





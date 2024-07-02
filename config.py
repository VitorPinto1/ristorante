from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
from werkzeug.security import generate_password_hash
from flask_bootstrap import Bootstrap
from datetime import datetime
from dotenv import load_dotenv
from flask_mail import Mail, Message
import os
import logging
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


load_dotenv()


app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRETKEY')

app.config['MYSQL_HOST'] = 'zle.h.filess.io'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = 'dbrestaurant_silkspeech'


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





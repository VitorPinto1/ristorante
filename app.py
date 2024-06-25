from flask import Flask, render_template, request, redirect, url_for, flash, session
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

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRETKEY')

app.config['MYSQL_HOST'] = 'zle.h.filess.io'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = 'dbrestaurant_silkspeech'


mysql = MySQL(app)
bcrypt = Bcrypt(app)

app.config['MAIL_DEFAULT_SENDER'] = 'staniaprojets@gmail.com'
app.config['MAIL_SERVER']='localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

bootstrap = Bootstrap(app)
ts = URLSafeTimedSerializer(app.secret_key)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return render_template('menu.html')

@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        try:
            name = request.form['name']
            total_person = int(request.form['totalPerson'])
            day = request.form['date']
            time = request.form['time']
            email = request.form['email']

            cursor = mysql.connection.cursor()
            cursor.execute('''
                SELECT SUM(totalPerson) FROM reservation
                WHERE day = %s AND time = %s
            ''', (day, time))
            total_people_reserved = cursor.fetchone()[0] or 0
            if total_people_reserved + total_person > 200:
                flash('Reservations exceed the limit of 200 people per hour.', 'danger')
                return redirect(url_for('reservation'))

            query = '''
                INSERT INTO reservation (name, totalPerson, day, time, email)
                VALUES (%s, %s, %s, %s, %s)
            '''
            data = (name, total_person, day, time, email)
            cursor.execute(query, data)
            reservation_id = cursor.lastrowid
            mysql.connection.commit()
            cursor.close()


            # confirmation email
            msg = Message('Reservation Confirmation',
                          recipients=[email])
            msg.body = f'Hello {name},\n\nYour reservation number {reservation_id} for {day} at {time} is confirmed. We look forward to serving you.\n\nBest regards,\nRistorante "Il Capo" Team'
            try:
                mail.send(msg)
                logging.info('Confirmation email sent successfully.')
                flash(f'Hello {name}, your reservation number {reservation_id} for {day} at {time} is confirmed. We have sent you an email as well. We look forward to serving you. Best regards, Ristorante "Il Capo" Team', 'success')
            except Exception as e:
                logging.error(f'Failed to send confirmation email: {e}')
                flash(f'Failed to send confirmation email: {e}', 'danger')


            return redirect(url_for('confirmation'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('reservation'))
    
    return render_template('reservation.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            password = request.form['password']

            cursor = mysql.connection.cursor()

            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                flash('Email address already exists', 'danger')
                cursor.close()
                return redirect(url_for('sign_up'))
            
            cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
            existing_user_name = cursor.fetchone()
            if existing_user_name:
                flash('Username already exists', 'danger')
                cursor.close()
                return redirect(url_for('sign_up'))

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
            
            mysql.connection.commit()
            cursor.close()

            token = ts.dumps(email, salt='email-confirm-key')
            
            confirm_url = url_for('confirm_email', token=token, _external=True)
            msg = Message('Confirm your email', recipients=[email])
            msg.body = f'Hello {name},\n\nPlease click the link to confirm your email address: {confirm_url}\n\nBest regards,\nRistorante "Il Capo" Team'
            try:
                mail.send(msg)
                logging.info('Confirmation email sent successfully.')
                flash(f'Hello {name}, please check your email to confirm your registration.', 'success')
            except Exception as e:
                logging.error(f'Failed to send confirmation email: {e}')
                flash(f'Failed to send confirmation email: {e}', 'danger')

            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('sign_up'))

    return render_template('sign_up.html')

@app.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt='email-confirm-key', max_age=3600)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('sign_up'))

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET active = %s WHERE email = %s", (True, email))
    mysql.connection.commit()
    cursor.close()

    flash('Your email has been confirmed. You can now log in.', 'success')
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            try:
                if bcrypt.check_password_hash(user[2], password):
                    session['user_id'] = user[0]
                    session['user_name'] = user[1]
                    flash('Login successful!', 'success')
                    return redirect(url_for('user_space'))
                else:
                    flash('Invalid email or password', 'danger')
            except ValueError as ve:
                logging.error(f'Error during password verification: {ve}')
                flash('There was an error with your login. Please try again.', 'danger')
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')




@app.route('/user_space')
def user_space():
    if 'user_id' not in session:
        flash('You need to login first', 'danger')
        return redirect(url_for('login'))
    return render_template('user_space.html', name=session.get('user_name'))


if __name__ == "__main__":
    app.run(debug=True)



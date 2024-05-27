from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
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

app.config['MAIL_DEFAULT_SENDER'] = 'staniaprojets@gmail.com'
app.config['MAIL_SERVER']='localhost'
app.config['MAIL_PORT'] = 1025
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

bootstrap = Bootstrap(app)

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
            msg.body = f'Hello {name},\n\nYour reservation (ID: {reservation_id}) for {day} at {time} is confirmed. We look forward to serving you.\n\nBest regards,\nRistorante "Il Capo" Team'
            try:
                mail.send(msg)
                logging.info('Confirmation email sent successfully.')
                flash('Reservation confirmed! A confirmation email has been sent.', 'success')
            except Exception as e:
                logging.error(f'Failed to send confirmation email: {e}')

                flash(f'Failed to send confirmation email: {e}', 'danger')


            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('index'))
    
    return render_template('reservation.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')




if __name__ == "__main__":
    app.run(debug=True)



"""
msg = Message('Confirmez votre compte', sender='mailtrap@demomailtrap.com', recipients=[email])
msg.body = f'Hello {name}, Your reservation {id} for {date} - {time} is confirmed.  We look forward to serving you at Ristorante "Il Capo". Best regards '
mail.send(msg) """
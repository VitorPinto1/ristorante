from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from datetime import datetime
from dotenv import load_dotenv
import os



app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRETKEY')

app.config['MYSQL_HOST'] = 'zle.h.filess.io'
app.config['MYSQL_PORT'] = 3307
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = 'dbrestaurant_silkspeech'


mysql = MySQL(app)



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
            person = request.form['name']
            total_person = int(request.form['totalPerson'])
            day = request.form['date']
            time = request.form['time']

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
                INSERT INTO reservation (person, totalPerson, day, time)
                VALUES (%s, %s, %s, %s)
            '''
            data = (person, total_person, day, time)
            cursor.execute(query, data)
            mysql.connection.commit()
            cursor.close()

           
            

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
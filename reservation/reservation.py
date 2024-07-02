from config import *



reservation_bp = Blueprint('reservation', __name__, template_folder='templates')


@reservation_bp.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        try:
            name = request.form['name']
            total_person = int(request.form['totalPerson'])
            day = request.form['date']
            time = request.form['time']
            email = request.form['email']
            user_id = session.get('user_id')

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
                INSERT INTO reservation (name, totalPerson, day, time, email, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            data = (name, total_person, day, time, email, user_id)
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
    
    user_name = session.get('user_name', '')
    user_email = session.get('user_email', '')
    
    return render_template('reservation.html' , user_name=user_name, user_email=user_email)


@reservation_bp.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')
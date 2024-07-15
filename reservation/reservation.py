from config import *

# Create a Blueprint named 'reservation' with templates located in the 'templates' folder
reservation_bp = Blueprint('reservation', __name__, template_folder='templates')

@reservation_bp.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        try:
            name = request.form['name']
            total_person = int(request.form['totalPerson'])
            day = request.form['date']
            time_str = request.form['time']
            email = request.form['email']
            user_id = session.get('user_id')

            # Validate required fields
            if not name or not total_person or not day or not time_str or not email:
                return render_template('reservation.html', error='All fields are required!'), 401
            reservation_date = datetime.strptime(day, '%Y-%m-%d').date()

            # Validate reservation date is not in the past
            if reservation_date < datetime.now().date():
                flash('Reservations cannot be made for past dates.', 'danger')
                return make_response(render_template('reservation.html'), 401)
            reservation_time = dt_time.fromisoformat(time_str)

            # Validate reservation time is within allowed hours
            if not (dt_time(12, 0) <= reservation_time <= dt_time(23, 59)):
                flash('Reservations can only be made between 12:00 and 24:00.', 'danger')
                return make_response(render_template('reservation.html'), 401)
            
            # Validate total persons does not exceed limit
            if total_person > 10:
                return render_template('reservation.html', error='Reservations cannot be made for more than 10 people.'), 401
            cursor = mysql.connection.cursor()
            cursor.execute('''
                SELECT SUM(totalPerson) FROM reservation
                WHERE day = %s AND time = %s
            ''', (day, time_str))
            total_people_reserved = cursor.fetchone()[0] or 0

            # Validate total reservations do not exceed restaurant capacity
            if total_people_reserved + total_person > 200:
                flash('Reservations exceed the limit of 200 people per hour.', 'danger')
                return redirect(url_for('reservation.reservation'))
            query = '''
                INSERT INTO reservation (name, totalPerson, day, time, email, user_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            '''
            data = (name, total_person, day, time_str, email, user_id)
            cursor.execute(query, data)
            reservation_id = cursor.lastrowid
            mysql.connection.commit()
            cursor.close()
            
            # Send confirmation email
            msg = Message('Reservation Confirmation',
                          recipients=[email])
            msg.body = f'Hello {name},\n\nYour reservation number {reservation_id} for {day} at {time_str} is confirmed. We look forward to serving you.\n\nBest regards,\nRistorante "Il Capo" Team'
            try:
                mail.send(msg)
                logging.info('Confirmation email sent successfully.')
                flash(f'Hello {name}, your reservation number {reservation_id} for {day} at {time_str} is confirmed. We have sent you an email as well. We look forward to serving you. Best regards, Ristorante "Il Capo" Team', 'success')
            except Exception as e:
                logging.error(f'Failed to send confirmation email: {e}')
                flash(f'Failed to send confirmation email: {e}', 'danger')
            return redirect(url_for('reservation.confirmation'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('reservation.reservation'))
    user_name = session.get('user_name', '')
    user_email = session.get('user_email', '')

    return render_template('reservation.html' , user_name=user_name, user_email=user_email)

@reservation_bp.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')



from config import *

# Create a Blueprint for user-related routes
user_bp = Blueprint('user', __name__, template_folder='templates')


def get_closest_reservations(user_id, limit=1):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('''
            SELECT id, totalPerson, day, time
            FROM reservation 
            WHERE day >= CURDATE() AND user_id = %s
            ORDER BY day ASC, time ASC 
            LIMIT %s
        ''', (user_id, limit))
        closest_reservations = cursor.fetchall()
        cursor.close()
        
        if not closest_reservations:
            return []
        
        reservations_list = []
        for reservation in closest_reservations:
            reservations_list.append({
                'id': reservation[0],
                'totalPerson': reservation[1],
                'day': reservation[2],
                'time': reservation[3]
            })
        return reservations_list
        
    except Exception as e:
        logging.error(f'Error fetching closest reservations: {e}')
        return []
    


@user_bp.route('/user_space')
def user_space():
    if 'user_id' not in session:
        flash('You need to login first', 'danger')
        return redirect(url_for('login.login'))

    user_id = session['user_id']
    user_name = session.get('user_name', '')
    user_email = session.get('user_email', '')
    closest_reservations = get_closest_reservations(user_id=user_id, limit=1)
    closest_reservation = closest_reservations[0] if closest_reservations else None
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM reservation WHERE user_id = %s ORDER BY day ASC, time ASC', (user_id,))
    reservations = cursor.fetchall()
    cursor.close()

    return render_template('user_space.html', user_name=user_name, user_email=user_email, closest_reservation=closest_reservation, reservations=reservations)


@user_bp.route('/change_password_page')
def change_password_page():
    if 'user_id' not in session:
        flash('You need to login first', 'danger')
        return redirect(url_for('login.login'))
    return render_template('password_change.html')


@user_bp.route('/change_password', methods=['POST'])
def change_password():
    if 'user_id' not in session:
        flash('You need to log in first', 'danger')
        return redirect(url_for('login.login'))
    user_id = session['user_id']
    current_password = request.form['currentPassword']
    new_password = request.form['newPassword']
    confirm_password = request.form['confirmPassword']
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT password FROM users WHERE id = %s', (user_id,))
    user = cursor.fetchone()
    cursor.close()

    if user and len(user) > 0:
        hashed_password = user[0]
    else:
        flash('Error retrieving user password.', 'danger')
        return redirect(url_for('user.change_password_page'))

    if not bcrypt.check_password_hash(hashed_password, current_password):
        flash('Current password is incorrect.', 'danger')
        return redirect(url_for('user.change_password_page'))

    if new_password != confirm_password:
        flash('New passwords do not match.', 'danger')
        return redirect(url_for('user.change_password_page'))

    new_hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE users SET password = %s WHERE id = %s', (new_hashed_password, user_id))
    mysql.connection.commit()
    cursor.close()
    flash('Password updated successfully.', 'success')
    return redirect(url_for('user.user_space'))

@user_bp.route('/reservation/<int:reservation_id>/delete', methods=['GET', 'POST'])
def delete_reservation(reservation_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM reservation WHERE id = %s', (reservation_id,))
    mysql.connection.commit()
    cursor.close()
    flash('Reservation deleted successfully.', 'success')
    return redirect(url_for('user.user_space'))

@user_bp.route('/reservation/<int:reservation_id>/modify', methods=['GET', 'POST'])
def modify_reservation(reservation_id):
    new_date = request.form['date']
    new_time = request.form['time']
    new_total_person = request.form['totalPerson']
    cursor = mysql.connection.cursor()
    cursor.execute('''
        UPDATE reservation
        SET day = %s, time = %s, totalPerson = %s
        WHERE id = %s
    ''', (new_date, new_time, new_total_person, reservation_id))
    mysql.connection.commit()
    cursor.close()
    flash('Reservation modified successfully.', 'success')
    return redirect(url_for('user.user_space'))

@user_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    return redirect(url_for('index'))






from config import *

# Create a Blueprint for user-related routes
user_bp = Blueprint('user', __name__, template_folder='templates')

@user_bp.route('/user_space')
def user_space():
    if 'user_id' not in session:
        flash('You need to login first', 'danger')
        return redirect(url_for('login.login'))
    user_id = session['user_id']
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM reservation WHERE user_id = %s', (user_id,))
    reservations = cursor.fetchall()
    cursor.close()
    return render_template('user_space.html', name=session.get('user_name'), reservations=reservations)

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
from config import *

signUp_bp = Blueprint('sign_up', __name__, template_folder='templates')

@signUp_bp.route('/sign_up', methods=['GET', 'POST'])
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
                return redirect(url_for('sign_up.sign_up'))
            
            cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
            existing_user_name = cursor.fetchone()
            if existing_user_name:
                flash('Username already exists', 'danger')
                cursor.close()
                return redirect(url_for('sign_up.sign_up'))

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            cursor.execute("INSERT INTO users (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_password))
            
            mysql.connection.commit()
            cursor.close()

            token = ts.dumps(email, salt='email-confirm-key')
            
            confirm_url = url_for('sign_up.confirm_email', token=token, _external=True)
            msg = Message('Confirm your email', recipients=[email])
            msg.body = f'Hello {name},\n\nPlease click the link to confirm your email address: {confirm_url}\n\nBest regards,\nRistorante "Il Capo" Team'
            try:
                mail.send(msg)
                logging.info('Confirmation email sent successfully.')
                flash(f'Hello {name}, please check your email to confirm your registration.', 'success')
            except Exception as e:
                logging.error(f'Failed to send confirmation email: {e}')
                flash(f'Failed to send confirmation email: {e}', 'danger')

            return redirect(url_for('index.index'))
        except Exception as e:
            flash(f'Error: {e}', 'danger')
            return redirect(url_for('sign_up.sign_up'))

    return render_template('sign_up.html')

@signUp_bp.route('/confirm/<token>')
def confirm_email(token):
    try:
        email = ts.loads(token, salt='email-confirm-key', max_age=3600)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('sign_up.sign_up'))

    cursor = mysql.connection.cursor()
    cursor.execute("UPDATE users SET active = %s WHERE email = %s", (True, email))
    mysql.connection.commit()
    cursor.close()

    flash('Your email has been confirmed. You can now log in.', 'success')
    return redirect(url_for('index.index'))
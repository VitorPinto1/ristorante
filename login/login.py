from config import *


login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/login', methods=['GET', 'POST'])
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
                    session['user_email'] = user[3]  
                    return redirect(url_for('user.user_space'))
                else:
                    flash('Invalid email or password', 'danger')
            except ValueError as ve:
                logging.error(f'Error during password verification: {ve}')
                flash('There was an error with your login. Please try again.', 'danger')
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')

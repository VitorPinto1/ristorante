from config import *


login_bp = Blueprint('login', __name__, template_folder='templates')

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']

        if not name or not password:
            flash('All fields are required!', 'danger')
            return make_response(render_template('login.html'), 401)

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
                    flash('Invalid name or password', 'danger')
                    return make_response(render_template('login.html'), 401)
            except ValueError as ve:
                logging.error(f'Error during password verification: {ve}')
                flash('There was an error with your login. Please try again.', 'danger')
                return make_response(render_template('login.html'), 401)
        else:
            flash('Invalid name or password', 'danger')
            return make_response(render_template('login.html'), 401)

    return render_template('login.html')

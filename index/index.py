from config import *

# Create a Blueprint named 'index' with templates located in the 'templates' folder
index_bp = Blueprint('index', __name__, template_folder='templates')

@index_bp.route('/')
def index():
    # Retrieve the user's name and email from the session
    user_name = session.get('user_name', '')
    user_email = session.get('user_email', '')
    return render_template('index.html', user_name=user_name, user_email=user_email)

@index_bp.route('/menu')
def menu():
    return render_template('menu.html')

@index_bp.route('/about_us')
def about_us():
    return render_template('about_us.html')

@index_bp.route('/reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        pass
    user_name = session.get('user_name', '')
    user_email = session.get('user_email', '')
    return render_template('reservation.html', user_name=user_name, user_email=user_email)
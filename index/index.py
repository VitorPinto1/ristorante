from config import *

index_bp = Blueprint('index', __name__, template_folder='templates')

@index_bp.route('/')
def index():
    return render_template('index.html')


@index_bp.route('/menu')
def menu():
    return render_template('menu.html')



@index_bp.route('/about_us')
def about_us():
    return render_template('about_us.html')
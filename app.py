from config import *

from login import login_bp
from sign_up import signUp_bp
from reservation import reservation_bp
from user import user_bp
from index import index_bp
from flask import render_template
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

app.register_blueprint(login_bp, url_prefix='/login')
app.register_blueprint(signUp_bp, url_prefix='/sign_up')
app.register_blueprint(reservation_bp, url_prefix='/reservation')
app.register_blueprint(user_bp, url_prefix='/user' )
app.register_blueprint(index_bp, url_prefix='/index')

@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)



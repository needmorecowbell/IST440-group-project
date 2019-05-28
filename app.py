from flask import Flask
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user 
from models.user import User


UPLOAD_FOLDER = 'uploads'
REPORT_FOLDER = 'reports'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# create some users with ids 1 to 20       
users = [User(id) for id in range(1, 21)]



from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_session import Session

# Initialize the Flask app
app = Flask(__name__)

# Application configuration
app.config['SECRET_KEY'] = 'your_secret_key'  # Make sure to replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calendar.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Security and session settings
app.config['SESSION_COOKIE_SECURE'] = False  # Ensure cookies are only sent over HTTPS in production
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protect against CSRF attacks
app.config['PREFERRED_URL_SCHEME'] = 'https'



# Configure server-side session storage
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/tmp/flask_sessions'  # You can specify any directory
app.config['SESSION_PERMANENT'] = False

# Initialize SQLAlchemy and Flask-Login
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Specifies which view is used for login redirection

# Handle reverse proxy setups (e.g., Nginx/Apache with HTTPS)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Load user using Flask-Login
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from app import routes, models

# Initialize Flask-Session
Session(app)
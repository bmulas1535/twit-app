from twitapp import routes
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = '1d06cefddc423f3464396352ac04df66'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app_data.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "You must be logged in to do that."
login_manager.login_message_category = "danger"

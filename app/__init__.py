from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = '123@21414#$4241'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///webar.db'
db = SQLAlchemy(app)
manager = LoginManager(app)

from app import routes

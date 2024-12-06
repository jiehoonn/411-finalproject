from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_session import Session
from datetime import timedelta

db = SQLAlchemy()
bcrypt = Bcrypt()
session = Session()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Session configuration
    app.config['SESSION_TYPE'] = 'sqlalchemy'
    app.config['SESSION_SQLALCHEMY'] = db
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    
    db.init_app(app)
    bcrypt.init_app(app)
    session.init_app(app)

    return app

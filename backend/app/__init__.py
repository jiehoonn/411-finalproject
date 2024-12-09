from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={
        r"/*": {
            "origins": "http://localhost:3000",
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    
    from routes.stocks import bp as stocks_bp
    app.register_blueprint(stocks_bp)
    
    return app


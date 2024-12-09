from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from .config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    CORS(app, origins="http://127.0.0.1:3000", supports_credentials=True)
    app.config.from_object(Config)
    
    db.init_app(app)
    bcrypt.init_app(app)
    
    from routes.stocks import bp as stocks_bp
    app.register_blueprint(stocks_bp)
    
    return app

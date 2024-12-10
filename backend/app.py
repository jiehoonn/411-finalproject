from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

from backend.routes.stocks import bp as stocks_bp
from backend.routes.stock import stock_blueprint
from backend.routes.auth_routes import auth_blueprint
from backend.routes.portfolio import portfolio_blueprint

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocktrading.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ALPHA_VANTAGE_API_KEY'] = os.getenv('ALPHA_VANTAGE_API_KEY')

    # allow frontend to access backend (CORS setup)
    CORS(app, origins="http://localhost:3000", supports_credentials=True)

    # initialize database
    db.init_app(app)

    # register blueprints
    app.register_blueprint(stock_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(stocks_bp)
    app.register_blueprint(portfolio_blueprint)

    return app

# app instance for WSGI server
app = create_app()

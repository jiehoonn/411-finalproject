from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from services.portfolio import PortfolioService
from services.alpha_vantage import AlphaVantageService

db = SQLAlchemy()
bcrypt = Bcrypt()
portfolio_service = PortfolioService()
alpha_vantage = AlphaVantageService()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    CORS(app, origins="http://localhost:3000", supports_credentials=True)
    
    db.init_app(app)
    bcrypt.init_app(app)
    
    from routes.dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)
    
    return app

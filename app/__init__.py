from backend.routes import user_routes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    bcrypt.init_app(app)

    from app.routes import portfolio_routes, trade_routes, stock_routes
    app.register_blueprint(user_routes.bp)
    app.register_blueprint(portfolio_routes.bp)
    app.register_blueprint(trade_routes.bp)
    app.register_blueprint(stock_routes.bp)

    return app

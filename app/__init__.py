from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from backend.routes.stocks import bp as stocks_bp

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    bcrypt.init_app(app)

    # app.register_blueprint(user_routes.bp)
    # app.register_blueprint(portfolio_routes.bp)
    # app.register_blueprint(trade_routes.bp)
    app.register_blueprint(stocks_bp)

    return app

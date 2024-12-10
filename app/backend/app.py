from flask import Flask
from backend.database import db
from app.backend.routes.stocks import stock_blueprint
from app.backend.routes.auth_routes import auth_blueprint
from backend.services.portfolio import portfolio_blueprint  # importing new portfolio blueprint

def create_app():
    app = Flask(__name__)
    #app.config.from_object('backend.config.Config')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'  # SQLite database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # disable modification tracking

    # initialize database
    db.init_app(app)

    # register Blueprints
    app.register_blueprint(stock_blueprint)
    app.register_blueprint(auth_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

# # app.py
# from flask import Flask
# from backend.database import db
# from backend.routes.stock import stock_blueprint
# from backend.routes.portfolio import portfolio_blueprint  # importing new portfolio blueprint
# from backend.routes.auth_routes import auth_blueprint

# def create_app():
#     app = Flask(__name__)

#     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_database.db'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#     db.init_app(app)

#     # Register Blueprints
#     app.register_blueprint(stock_blueprint)
#     app.register_blueprint(portfolio_blueprint)  # register portfolio blueprint
#     app.register_blueprint(auth_blueprint)

#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)


#from flask import Flask, request, jsonify
#from flask_cors import CORS
#from flask_sqlalchemy import SQLAlchemy
#from datetime import datetime, timedelta
#from dotenv import load_dotenv
#from services.alpha_vantage import AlphaVantageService
#import os
#import requests


#load_dotenv()

#app = Flask(__name__)
#CORS(app)

# Database configuration
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocktrading.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#db = SQLAlchemy(app)

# Alpha Vantage API configuration
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
cache = {}

# TO DO FIX

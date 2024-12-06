from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from routes.stocks import bp as stocks_bp
from flask_cors import CORS
import os

db = SQLAlchemy()

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocktrading.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')

db.init_app(app)

app.register_blueprint(stocks_bp)
# app.register_blueprint(users_bp)
for rule in app.url_map.iter_rules():
    print(f"{rule.endpoint}: {rule.rule}")

if __name__ == "__main__":
    app.run(debug=True)

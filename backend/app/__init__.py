from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)

    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy'})  # Return JSON response

    from app.routes import auth, stocks
    app.register_blueprint(auth.bp)
    app.register_blueprint(stocks.bp)

    with app.app_context():
        db.create_all()

    return app
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from dotenv import load_dotenv
from services.alpha_vantage import AlphaVantageService
import os
import requests


load_dotenv()

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocktrading.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Alpha Vantage API configuration
ALPHA_VANTAGE_API_KEY = os.getenv('ALPHA_VANTAGE_API_KEY')
cache = {}

@app.route('/lookup-stock', methods=['GET'])
def lookup_stock():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "No symbol given.."}), 400

    if symbol in cache:
        cached_data = cache[symbol]
        if datetime.now() - cached_data['timestamp'] < timedelta(minutes=10):
            return jsonify(cached_data['data'])

    av_client = AlphaVantageService()
    try:
        res_data = av_client.get_stock_quote(symbol)
        if "Global Quote" not in res_data or not res_data["Global Quote"]:
            return jsonify({"error": "No data found for the given symbol"}), 404

        current_price = res_data["Global Quote"].get("05. price", "N/A")
        volume = res_data["Global Quote"].get("06. volume", "N/A")
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error getting price: {str(e)}"}), 500

    try:
        hist_data = av_client.get_time_series_daily(symbol)
        if "Time Series (Daily)" not in hist_data:
            return jsonify({"error": "No historical data found for given symbol"}), 404

        daily_data = hist_data["Time Series (Daily)"]
        last_7_days = [
            {"date": date, "close": values["4. close"]}
            for date, values in list(daily_data.items())[:7]
        ]
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching historical data: {str(e)}"}), 500

    data = {
        "symbol": symbol,
        "current_price": current_price,
        "volume": volume,
        "last_7_days": last_7_days
    }

    cache[symbol] = {
        "timestamp": datetime.now(),
        "data": data
    }

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)

from flask import Blueprint, request, jsonify
from flask_cors import CORS
from services.alpha_vantage import AlphaVantageService
from datetime import datetime, timedelta
import requests
from services.portfolio import PortfolioService
from app.models import User, Portfolio, db


bp = Blueprint('stocks', __name__)
CORS(bp)
alpha_vantage = AlphaVantageService()
portfolio_service = PortfolioService()

@bp.route('/api/stock/quote/<symbol>')
def get_quote(symbol):
    """
    Get the current stock data for the given symbol.

    Args:
        symbol (str): The stock symbol for which the quote is fetched.

    Returns:
        quote: Stock data in JSON format.
    """
    quote = alpha_vantage.get_stock_quote(symbol)
    return jsonify(quote)


@bp.route('/api/stock/value/<symbol>/<int:shares>')
def calculate_value(symbol, shares):
    """
    Calculates the value of a stock position based on the current stock quote.

    Args:
        symbol (str): The stock symbol.
        shares (int): The number of shares owned.

    Returns:
        value: The calculated value of the stock position in JSON format.
    """
    quote = alpha_vantage.get_stock_quote(symbol)
    price = float(quote['Global Quote']['05. price'])
    value = price * shares
    return jsonify({'value': value})


@bp.route('/lookup-stock', methods=['GET'])
def lookup_stock():
    """
    Find and return the current stock data and market status for a given symbol

    Args:
        symbol (str): The stock symbol.

    Returns:
        data: Stock data in JSON format or error message.
    """
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "No symbol given.."}), 400

    try:
        res_data = alpha_vantage.get_stock_quote(symbol)
        if "Global Quote" not in res_data or not res_data["Global Quote"]:
            return jsonify({"error": "No data found for the given symbol"}), 404

        current_price = res_data["Global Quote"].get("05. price", "N/A")
        volume = res_data["Global Quote"].get("06. volume", "N/A")

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error getting price: {str(e)}"}), 500

    try:
        hist_data = alpha_vantage.get_time_series_daily(symbol)
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

    return jsonify(data)


@bp.route('/historical-data', methods=['GET'])
def historical_data():
    """
    Get the historical trends data for the stock symbol within a specified time range.

    Args:
        symbol (str): The stock symbol.
        range (str): Time range for the historical data (e.g., '1d', '10d', '1m').

    Returns:
        main_data: Historical stock trend data in JSON format or error message.
    """
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "Stock name required"}), 400

    range = request.args.get('range', '1m')
    ranges = {
        '1d': {
            'endpoint': 'TIME_SERIES_INTRADAY',
            'interval': '60min',
            'days': 1
        },
        '10d': {
            'endpoint': 'TIME_SERIES_DAILY',
            'days': 10
        },
        '1m': {
            'endpoint': 'TIME_SERIES_DAILY',
            'days': 30
        },
        '6m': {
            'endpoint': 'TIME_SERIES_MONTHLY',
            'months': 6
        },
        '1y': {
            'endpoint': 'TIME_SERIES_MONTHLY',
            'months': 12
        }
    }

    dets = ranges.get(range, ranges['1m'])

    if dets['endpoint'] == 'TIME_SERIES_INTRADAY':
        hist_data = alpha_vantage.get_time_series_intraday(symbol, dets['interval'])
    elif dets['endpoint'] == 'TIME_SERIES_DAILY':
        hist_data = alpha_vantage.get_time_series_daily(symbol)
    elif dets['endpoint'] == 'TIME_SERIES_MONTHLY':
        hist_data = alpha_vantage.get_time_series_monthly(symbol)

    time_series = hist_data.get(f'Time Series (60min)') or hist_data.get('Time Series (Daily)') or hist_data.get('Monthly Time Series')

    if not time_series:
        return jsonify({"error": "Invalid data retrieved!"}), 500

    main_data = []
    today = datetime.today()

    for date, stats in sorted(time_series.items(), reverse=True):
        date_obj = datetime.strptime(date.split()[0], '%Y-%m-%d')
        condition = (today - date_obj).days <= dets['days'] if 'days' in dets else (today - date_obj).days <= dets['months'] * 30
        if condition:
            main_data.append({"date": date,"close": float(stats["4. close"])})

    return jsonify(main_data)

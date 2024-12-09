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

    try:
        # get market status data
        md = alpha_vantage.get_market_status()
        ms = []
        if "market_status" in md:
            for m in md["market_status"]:
                ms.append({
                    "market_type": m.get("market_type", "Unknown"),
                    "region": m.get("region", "Unknown"),
                    "primary_exchanges": m.get("primary_exchanges", "Unknown"),
                    "local_open": m.get("local_open", "Unknown"),
                    "local_close": m.get("local_close", "Unknown"),
                    "current_status": m.get("current_status", "Unknown")
                })
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching market status: {str(e)}"}), 500

    data = {
        "symbol": symbol,
        "current_price": current_price,
        "volume": volume,
        "last_7_days": last_7_days,
        "market_status": ms
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

@bp.route('/api/buy-stock', methods=['POST'])
def buy_stock():
    data = request.json
    symbol = data.get('symbol')
    quantity = int(data.get('quantity'))
    
    print(f"Attempting to buy {quantity} shares of {symbol}")  # Debug print

    quote = alpha_vantage.get_stock_quote(symbol)
    print(f"API Response: {quote}")  # Debug print

    if 'Information' in quote:
        return jsonify({'success': False, 'error': 'API rate limit reached. Please try again later.'}), 429
        
    if 'Global Quote' not in quote:
        return jsonify({'success': False, 'error': 'Invalid stock symbol or API error'}), 400

    current_price = float(quote['Global Quote']['05. price'])
    total_cost = current_price * quantity
    
    user = User.query.first()
    print(f"User balance before purchase: {user.balance}")  # Debug print
    
    if user.balance >= total_cost:
        existing_position = Portfolio.query.filter_by(
            user_id=user.id, symbol=symbol
        ).first()
        
        if existing_position:
            existing_position.quantity += quantity
        else:
            new_position = Portfolio(
                user_id=user.id,
                symbol=symbol,
                quantity=quantity,
                purchase_price=current_price
            )
            db.session.add(new_position)
            
        user.balance -= total_cost
        db.session.commit()
        
        total_value = sum(portfolio_service.calculate_holding_value(pos) for pos in user.portfolio)
        
        return jsonify({
            'success': True,
            'new_balance': user.balance,
            'portfolio_value': total_value
        })
    
    return jsonify({'success': False, 'error': 'Insufficient funds'})


@bp.route('/api/sell-stock', methods=['POST'])
def sell_stock():
    data = request.json
    symbol = data.get('symbol')
    quantity = int(data.get('quantity'))
    
    quote = alpha_vantage.get_stock_quote(symbol)
    current_price = float(quote['Global Quote']['05. price'])
    total_value = current_price * quantity
    
    user = User.query.first()
    position = Portfolio.query.filter_by(user_id=user.id, symbol=symbol).first()
    
    if position and position.quantity >= quantity:
        position.quantity -= quantity
        user.balance += total_value
        
        if position.quantity == 0:
            db.session.delete(position)
            
        db.session.commit()
        
        return jsonify({
            'success': True,
            'new_balance': user.balance,
            'portfolio_value': portfolio_service.calculate_holding_value(user.id)
        })
    
    return jsonify({'success': False, 'error': 'Insufficient shares'})

@bp.route('/api/portfolio-status')
def get_portfolio_status():
    user = User.query.first()
    print(f"User balance: {user.balance}")  # Debug print
    
    # Calculate total portfolio value
    total_value = 0
    for position in user.portfolio:
        total_value += portfolio_service.calculate_holding_value(position)
    
    return jsonify({
        'balance': user.balance,
        'portfolio_value': total_value
    })

from flask import Blueprint, request, jsonify
from flask_cors import CORS
from services.alpha_vantage import AlphaVantageService
from datetime import datetime
from app.models import User, Portfolio, db
import logging
from logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)

bp = Blueprint('stocks', __name__)
CORS(bp)

alpha_vantage = AlphaVantageService()

@bp.route('/api/stock/quote/<symbol>')
def get_quote(symbol):
    """
    Get the current stock data for the given stock symbol.

    Args:
        symbol (str): The stock symbol for which the quote (i.e data) is to be fetched.

    Returns:
        jsonify: The stock data in JSON format, or error message.

    Raises:
        Exception: If an error occurs while fetching the stock quote.
    """
    logger.info(f"Fetching stock info for: {symbol}")
    try:
        quote = alpha_vantage.get_stock_quote(symbol)
        logger.info(f"Stock info fetched successfully: {quote}")
        return jsonify(quote)
    except Exception as e:
        logger.error(f"Error fetching stock info for {symbol}: {str(e)}")
        return jsonify({'error': 'Failed to fetch stock quote'}), 500



@bp.route('/api/stock/value/<symbol>/<int:shares>')
def calculate_value(symbol, shares):
    """
    Calculates the value of a stock position based on the current stock quote.

    Args:
        symbol (str): The stock symbol.
        shares (int): The number of shares owned.

    Returns:
        value: The value of the stock position in JSON format or error message.

    Raises:
        Exception: If an error occurs while calculating the stock value.
    """
    logger.info(f"Calculating stock value for symbol with shares: {symbol, shares}")
    try:
        quote = alpha_vantage.get_stock_quote(symbol)
        price = float(quote['Global Quote']['05. price'])
        value = price * shares
        logger.info(f"Calculated value: {value}")
        return jsonify({'value': value})
    except Exception as e:
        logger.error(f"Error in calculating stock value for {symbol}: {str(e)}")
        return jsonify({'error': 'Failed to calculate stock value'}), 500



@bp.route('/lookup-stock', methods=['GET'])
def lookup_stock():
    """
    Find and return the current stock data and market status for a given symbol.

    Args:
        symbol (str): The stock symbol.

    Returns:
        data: The stock data in JSON format or error message.

    Raises:
        ValueError: If no symbol is provided in the input or no data is found for a given symbol. ????
        Exception: If an error occurs while fetching the stock or market status.
    """
    symbol = request.args.get('symbol')
    if not symbol:
        logger.warning("No symbol given for lookup in input!")
        return jsonify({"error": "No symbol given"}), 400

    logger.info(f"Looking up information for stock symbol: {symbol}")
    try:
        res_data = alpha_vantage.get_stock_quote(symbol)

        logger.debug(f"Stock info: {res_data}")
        if "Global Quote" not in res_data or not res_data["Global Quote"]:
            logger.warning(f"No data found for symbol: {symbol}")
            return jsonify({"error": "No data found for the given symbol"}), 404

        current_price = res_data["Global Quote"].get("05. price", "N/A")
        volume = res_data["Global Quote"].get("06. volume", "N/A")
        logger.debug(f"Price and Volume: {current_price, volume}")

    except Exception as e:
        logger.error(f"Error fetching stock lookup for {symbol}: {str(e)}")
        return jsonify({"error": f"Error getting stock data: {str(e)}"}), 500

    logger.info("Looking up global market status")
    try:
        md = alpha_vantage.get_market_status()
        ms = []
        if "markets" in md:
            for m in md["markets"]:
                ms.append({
                    "market_type": m.get("market_type", "Unknown"),
                    "region": m.get("region", "Unknown"),
                    "current_status": m.get("current_status", "Unknown")
                })
        logger.debug(f"Market status: {ms}")
    except Exception as e:
        logger.error(f"Error fetching market status: {str(e)}")
        return jsonify({"error": "Error getting market status"}), 500

    data = {
        "symbol": symbol,
        "current_price": current_price,
        "volume": volume,
        "market_status": ms
    }
    return jsonify(data)



@bp.route('/historical-data', methods=['GET'])
def historical_data():
    """
    Get the historical trends data for the stock symbol within a specified time range.

    Args:
        symbol (str): The stock symbol.
        range (str): The time range for the historical data (e.g., '1d', '10d', '1m').

    Returns:
        main_data: The historical stock trend data in JSON format or error message.

    Raises:
        ValueError: If no symbol is provided in the input or an invalid data is retrieved. ???
        Exception: If an error occurs while fetching the historical trend data.
    """
    symbol = request.args.get('symbol')
    if not symbol:
        logger.warning("No symbol given for historical in input!")
        return jsonify({"error": "No symbol given.."}), 400

    logger.info(f"Fetching historical trend data for symbol: {symbol}, range: {range}")
    range = request.args.get('range', '1m')
    range_mapping = {
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

    try:
        dets = range_mapping.get(range, range_mapping['1m'])
        if dets['endpoint'] == 'TIME_SERIES_INTRADAY':
            hist_data = alpha_vantage.get_time_series_intraday(symbol, dets['interval'])
        elif dets['endpoint'] == 'TIME_SERIES_DAILY':
            hist_data = alpha_vantage.get_time_series_daily(symbol)
        elif dets['endpoint'] == 'TIME_SERIES_MONTHLY':
            hist_data = alpha_vantage.get_time_series_monthly(symbol)

        time_series = hist_data.get(f'Time Series (60min)') or hist_data.get('Time Series (Daily)') or hist_data.get('Monthly Time Series')
        logger.debug(f"Trend data for {symbol} range {dets}: {time_series}")

        if not time_series:
            logger.error("Invalid data for historical data")
            return jsonify({"error": "Invalid data retrieved!"}), 500

        main_data = []
        today = datetime.today()

        for date, stats in sorted(time_series.items(), reverse=True):
            date_obj = datetime.strptime(date.split()[0], '%Y-%m-%d')
            condition = (today - date_obj).days <= dets['days'] if 'days' in dets else (today - date_obj).days <= dets['months'] * 30
            if condition:
                main_data.append({"date": date,"close": float(stats["4. close"])})

        return jsonify(main_data)

    except Exception as e:
        logger.error(f"Error fetching historical trend data: {str(e)} for symbol {symbol} of range {range}")
        return jsonify({"error": "Failed to fetch historical trend data"}), 500



@bp.route('/api/portfolio-status/<int:user_id>')
def get_portfolio_status(user_id):
    """
    Get the portfolio status i.e account balance and portfolio value for a user.

    Args:
        user_id (int): The user's ID.

    Returns:
        jsonify: The user's balance and portfolio value in JSON format, or error message.

    Raises:
        ValueError: If no user is found for the given ID.  ???
        Exception: If an error occurs while fetching portfolio data.
    """
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'No user found'}), 404

    total_value = 0
    for position in user.portfolio:
        quote = alpha_vantage.get_stock_quote(position.symbol)
        if 'Global Quote' in quote:
            current_price = float(quote['Global Quote']['05. price'])
            total_value += current_price * position.quantity

    return jsonify({
        'balance': user.balance,
        'portfolio_value': total_value
    })



@bp.route('/api/buy-stock', methods=['POST'])
def buy_stock():
    """
    Buy stock(s) for a user and update portfolio value and account balance.

    Args:
        symbol (str): The stock symbol.
        quantity (int): The number of shares to buy.
        userId (int): The user's ID.

    Returns:
        jsonify: The user's updated balance and portfolio value in JSON format, or error message.

    Raises:
        ValueError: If the input data is invalid, user is not found or insufficient funds for buying the stocks.
        Exception: If an error occurs while buying stock or updating portfolio.
    """
    data = request.json
    symbol = data.get('symbol')
    quantity = int(data.get('quantity', 0))
    user_id = data.get('userId')

    if not symbol or quantity <= 0 or not user_id:
        return jsonify({'success': False, 'error': 'Invalid input'}), 400

    quote = alpha_vantage.get_stock_quote(symbol)
    if 'Global Quote' not in quote:
        return jsonify({'success': False, 'error': 'Invalid stock symbol'}), 400

    current_price = float(quote['Global Quote']['05. price'])
    total_cost = current_price * quantity

    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404

    if user.balance < total_cost:
        return jsonify({'success': False, 'error': 'Insufficient funds'}), 400

    try:
        # Update or create position
        position = Portfolio.query.filter_by(user_id=user.id, symbol=symbol).first()
        if position:
            position.quantity += quantity
        else:
            position = Portfolio(
            user_id=user.id,
            symbol=symbol,
            quantity=quantity,
            purchase_price=current_price
            )
            db.session.add(position)

        user.balance -= total_cost
        db.session.commit()

        return jsonify({
        'success': True,
        'new_balance': user.balance,
        'portfolio_value': total_cost
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500



@bp.route('/api/sell-stock', methods=['POST'])
def sell_stock():
    """
    Sell stock(s) for a user and update portfolio value and account balance.

    Args:
        symbol (str): The stock symbol.
        quantity (int): The number of shares to sell.
        userId (int): The user's ID.

    Returns:
        jsonify: The user's updated balance and portfolio value in JSON format, or error message.

    Raises:
        ValueError: If the input data is invalid, user is not found or insufficient funds for selling the stocks.
        Exception: If an error occurs while selling stock or updating portfolio.
    """
    data = request.json
    symbol = data.get('symbol')
    quantity = int(data.get('quantity', 0))
    user_id = data.get('userId')

    if not symbol or quantity <= 0 or not user_id:
        return jsonify({'success': False, 'error': 'Invalid input'}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({'success': False, 'error': 'User not found'}), 404

    position = Portfolio.query.filter_by(user_id=user.id, symbol=symbol).first()
    if not position or position.quantity < quantity:
        return jsonify({'success': False, 'error': 'Insufficient shares'}), 400

    quote = alpha_vantage.get_stock_quote(symbol)
    if 'Global Quote' not in quote:
        return jsonify({'success': False, 'error': 'Invalid stock symbol'}), 400

    current_price = float(quote['Global Quote']['05. price'])
    total_value = current_price * quantity

    try:
        position.quantity -= quantity
        user.balance += total_value

        if position.quantity == 0:
            db.session.delete(position)

        db.session.commit()

        return jsonify({
            'success': True,
            'new_balance': user.balance,
            'portfolio_value': total_value
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

from flask import Blueprint, request, jsonify
from flask_cors import CORS
from services.alpha_vantage import AlphaVantageService
from datetime import datetime, timedelta
import requests
from services.portfolio import PortfolioService
from app.models import User, Portfolio, db
import logging
from ..logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)

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
    logger.info(f"Fetching stock info for: {symbol}")
    try:
        quote = alpha_vantage.get_stock_quote(symbol)
        logger.debug(f"Stock info fetched successfully: {quote}")
        return jsonify(quote)
    except Exception as e:
        logger.error(f"Error fetching stock quote for {symbol}: {str(e)}")
        return jsonify({'error': 'Failed to fetch stock quote'}), 500



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
    logger.info(f"Finding stock value for symbol with shares: {symbol, shares}")
    try:
        quote = alpha_vantage.get_stock_quote(symbol)
        price = float(quote['Global Quote']['05. price'])
        value = price * shares
        logger.debug(f"Calculated value: {value}")
        return jsonify({'value': value})
    except Exception as e:
        logger.error(f"Error in calculating stock value for {symbol}: {str(e)}")
        return jsonify({'error': 'Failed to calculate stock value'}), 500



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
                    # "local_open": m.get("local_open", "Unknown"),
                    # "local_close": m.get("local_close", "Unknown"),
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
        range (str): Time range for the historical data (e.g., '1d', '10d', '1m').

    Returns:
        main_data: Historical stock trend data in JSON format or error message.
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



@bp.route('/api/buy-stock', methods=['POST'])
def buy_stock():
    data = request.json
    symbol = data.get('symbol', None)
    quantity = int(data.get('quantity', None))

    if not symbol or quantity:
        logger.warning("No symbol/quantity given for buying stock!")
        return jsonify({"error": "No symbol/quantity given in buying"}), 400

    logger.info(f"Buy stock: symbol={symbol}, quantity={quantity}")
    logger.info(f"Fetching stock info for symbol: {symbol}")
    quote = alpha_vantage.get_stock_quote(symbol)
    logger.debug(f"Stock info: {quote}")

    if 'Information' in quote:
        logger.warning("API Rate Limit reached!")
        return jsonify({'success': False, 'error': 'API rate limit reached. Please try again later.'}), 429

    if 'Global Quote' not in quote:
        logger.error(f"Invalid stock symbol or API error for symbol: {symbol}")
        return jsonify({'success': False, 'error': 'Invalid stock symbol or API error'}), 400

    current_price = float(quote['Global Quote']['05. price'])
    total_cost = current_price * quantity
    logger.debug(f"Total Cost of Buying: {total_cost}")

    user = User.query.first()
    logger.debug(f"User: {user} Current balance: {user.balance}")

    if user.balance >= total_cost:
        logger.info("Sufficient balance, movng forward..")
        existing_position = Portfolio.query.filter_by(
            user_id=user.id, symbol=symbol
        ).first()

        if existing_position:
            logger.debug(f"Already exists = {existing_position}")
            existing_position.quantity += quantity
        else:
            logger.debug("Creating new portfolio entry")
            new_position = Portfolio(
                user_id=user.id,
                symbol=symbol,
                quantity=quantity,
                purchase_price=current_price
            )
            db.session.add(new_position)

        user.balance -= total_cost
        db.session.commit()
        logger.info("Transaction committed to db")

        total_value = sum(portfolio_service.calculate_holding_value(pos) for pos in user.portfolio)
        logger.debug(f"Calculated portfolio value: {total_value}")

        return jsonify({
            'success': True,
            'new_balance': user.balance,
            'portfolio_value': total_value
        })

    return jsonify({'success': False, 'error': 'Insufficient funds'})





@bp.route('/api/sell-stock', methods=['POST'])
def sell_stock():
    data = request.json
    symbol = data.get('symbol', None)
    quantity = int(data.get('quantity', None))

    if not symbol or quantity:
        logger.warning("No symbol/quantity given for selling stock!")
        return jsonify({"error": "No symbol/quantity given in selling"}), 400

    logger.info(f"Sell stock: symbol={symbol}, quantity={quantity}")
    logger.info(f"Fetching stock quote for symbol: {symbol}")
    quote = alpha_vantage.get_stock_quote(symbol)

    if 'Information' in quote:
        logger.warning("API rate limit reached")
        return jsonify({'success': False, 'error': 'API rate limit reached'}), 429

    current_price = float(quote['Global Quote']['05. price'])
    total_value = current_price * quantity
    logger.debug(f"Total value of sale: {total_value}")

    user = User.query.first()
    position = Portfolio.query.filter_by(user_id=user.id, symbol=symbol).first()
    logger.debug(f"User: {user} Current portfolio: {user.portfolio}")

    if position and position.quantity >= quantity:
        logger.info("Sufficient shares available, moving forward")
        position.quantity -= quantity
        user.balance += total_value

        if position.quantity == 0:
            logger.debug("Position quantity is zero, removing position from portfolio")
            db.session.delete(position)

        db.session.commit()
        logger.info("Transaction committed to db")

        total_portfolio_value = sum(portfolio_service.calculate_holding_value(pos) for pos in user.portfolio)
        logger.debug(f" Portfolio value after sale: {total_portfolio_value}")

        return jsonify({
            'success': True,
            'new_balance': user.balance,
            'portfolio_value': total_portfolio_value
        })

    logger.warning("Insufficient shares for sale")
    return jsonify({'success': False, 'error': 'Insufficient shares'})



@bp.route('/api/portfolio-status')
def get_portfolio_status():
    logger.info("Fetching portfolio status")
    user = User.query.first()
    logger.debug(f"User: {user} Current balance: {user.balance}")

    total_value = 0
    for position in user.portfolio:
        total_value += portfolio_service.calculate_holding_value(position)
    logger.debug(f"Total portfolio value: {total_value}")

    return jsonify({
        'balance': user.balance,
        'portfolio_value': total_value
    })

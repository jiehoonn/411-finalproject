from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models import db, User, Portfolio
from app.services.alpha_vantage import AlphaVantageService
from datetime import datetime
import requests

bp = Blueprint('stocks', __name__)
CORS(bp)

alpha_vantage = AlphaVantageService()

@bp.route('/api/stock/quote/<symbol>')
def get_quote(symbol):
    """Get stock quote for given symbol"""
    quote = alpha_vantage.get_stock_quote(symbol)
    return jsonify(quote)

@bp.route('/api/portfolio-status')
def get_portfolio_status():
    """Get user's portfolio status"""
    user = User.query.first()
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
    """Buy stock endpoint"""
    data = request.json
    symbol = data.get('symbol')
    quantity = int(data.get('quantity', 0))

    if not symbol or quantity <= 0:
        return jsonify({'success': False, 'error': 'Invalid input'}), 400

    quote = alpha_vantage.get_stock_quote(symbol)
    if 'Global Quote' not in quote:
        return jsonify({'success': False, 'error': 'Invalid stock symbol'}), 400

    current_price = float(quote['Global Quote']['05. price'])
    total_cost = current_price * quantity

    user = User.query.first()
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
    """Sell stock endpoint"""
    data = request.json
    symbol = data.get('symbol')
    quantity = int(data.get('quantity', 0))

    if not symbol or quantity <= 0:
        return jsonify({'success': False, 'error': 'Invalid input'}), 400

    user = User.query.first()
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
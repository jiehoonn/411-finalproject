from flask import Blueprint, request, jsonify
from middleware.auth import login_required
from services.portfolio import PortfolioService
from services.alpha_vantage import AlphaVantageService

bp = Blueprint('trade', __name__)
portfolio_service = PortfolioService()
alpha_vantage = AlphaVantageService()

@bp.route('/trade', methods=['POST'])
@login_required
def execute_trade():
    data = request.json
    user = request.user
    symbol = data.get('symbol')
    action = data.get('action')
    
    try:
        # Get current stock price
        quote = alpha_vantage.get_stock_quote(symbol)
        current_price = float(quote['Global Quote']['05. price'])
        
        if action == 'buy':
            if 'shares' in data:
                shares = float(data['shares'])
                cost = shares * current_price
                if cost > user.balance:
                    return jsonify({'error': 'Insufficient funds'}), 400
                    
                portfolio_service.buy_shares(
                    user_id=user.id,
                    symbol=symbol,
                    shares=shares,
                    price=current_price
                )
            else:
                amount = float(data['amount'])
                if amount > user.balance:
                    return jsonify({'error': 'Insufficient funds'}), 400
                    
                shares = amount / current_price
                portfolio_service.buy_shares(
                    user_id=user.id,
                    symbol=symbol,
                    shares=shares,
                    price=current_price
                )
                
        elif action == 'sell':
            shares = float(data['shares'])
            portfolio_service.sell_shares(
                user_id=user.id,
                symbol=symbol,
                shares=shares,
                price=current_price
            )
            
        return jsonify({
            'message': f'Successfully {action}ed {symbol}',
            'transaction': {
                'symbol': symbol,
                'shares': shares,
                'price': current_price
            }
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


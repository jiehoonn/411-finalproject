import pytest
from flask import Flask
from unittest.mock import patch
from datetime import datetime
from backend.app.models import db, User, Portfolio, StockTransaction
from backend.app.routes.stocks import bp as stocks_bp
from backend.app import create_app

# Mock API responses
MOCK_STOCK_PRICE = {
    "Global Quote": {
        "05. price": "150.00",
        "10. change percent": "1.5000%"
    }
}

MOCK_HISTORICAL_DATA = {
    "Time Series (Daily)": {
        "2024-01-01": {
            "4. close": "150.00"
        }
    }
}

@pytest.fixture
def app():
    """Create test Flask app"""
    app = create_app('testing')
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'TESTING': True,
        'SECRET_KEY': 'test_secret_key'
    })
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client, test_user):
    """Create authenticated headers"""
    response = client.post('/api/auth/login', json={
        'username': test_user['username'],
        'password': test_user['password']
    })
    token = response.get_json()['token']
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture
def test_user():
    """Create test user with balance"""
    return {
        'username': 'testtrader',
        'email': 'trader@test.com',
        'password': 'Test123!',
        'balance': 10000.00
    }

class TestStockPurchase:
    @patch('backend.app.routes.stocks.get_stock_price')
    def test_successful_stock_purchase(self, mock_price, client, auth_headers, test_user):
        """Test buying stocks successfully"""
        mock_price.return_value = float(MOCK_STOCK_PRICE['Global Quote']['05. price'])
        
        response = client.post('/api/stocks/buy', 
            json={
                'symbol': 'AAPL',
                'quantity': 10
            },
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Stock purchased successfully'
        assert 'transaction_id' in data
        
        # Verify portfolio update
        portfolio = Portfolio.query.filter_by(user_id=test_user['id']).first()
        assert portfolio.quantity == 10
        assert portfolio.symbol == 'AAPL'

    def test_insufficient_funds(self, client, auth_headers):
        """Test buying stocks with insufficient funds"""
        response = client.post('/api/stocks/buy',
            json={
                'symbol': 'AAPL',
                'quantity': 1000
            },
            headers=auth_headers
        )
        
        assert response.status_code == 400
        assert 'Insufficient funds' in response.get_json()['error']

class TestStockSale:
    @patch('backend.app.routes.stocks.get_stock_price')
    def test_successful_stock_sale(self, mock_price, client, auth_headers):
        """Test selling stocks successfully"""
        mock_price.return_value = float(MOCK_STOCK_PRICE['Global Quote']['05. price'])
        
        # First buy some stocks
        client.post('/api/stocks/buy',
            json={'symbol': 'AAPL', 'quantity': 10},
            headers=auth_headers
        )
        
        # Then sell them
        response = client.post('/api/stocks/sell',
            json={'symbol': 'AAPL', 'quantity': 5},
            headers=auth_headers
        )
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Stock sold successfully'
        assert 'transaction_id' in data

        # Verify portfolio update
        portfolio = Portfolio.query.filter_by(symbol='AAPL').first()
        assert portfolio.quantity == 5

class TestPortfolio:
    def test_get_portfolio(self, client, auth_headers):
        """Test retrieving user portfolio"""
        response = client.get('/api/stocks/portfolio', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'portfolio' in data
        assert isinstance(data['portfolio'], list)

    @patch('backend.app.routes.stocks.get_stock_price')
    def test_portfolio_value(self, mock_price, client, auth_headers):
        """Test calculating portfolio value"""
        mock_price.return_value = float(MOCK_STOCK_PRICE['Global Quote']['05. price'])
        
        response = client.get('/api/stocks/portfolio/value', headers=auth_headers)
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'total_value' in data
        assert isinstance(data['total_value'], float)

class TestStockData:
    @patch('backend.app.routes.stocks.get_stock_price')
    def test_get_stock_price(self, mock_price, client):
        """Test getting current stock price"""
        mock_price.return_value = float(MOCK_STOCK_PRICE['Global Quote']['05. price'])
        
        response = client.get('/api/stocks/price/AAPL')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'price' in data
        assert isinstance(data['price'], float)

    @patch('backend.app.routes.stocks.get_historical_data')
    def test_get_historical_data(self, mock_historical, client):
        """Test getting historical stock data"""
        mock_historical.return_value = MOCK_HISTORICAL_DATA
        
        response = client.get('/api/stocks/historical/AAPL?days=30')
        
        assert response.status_code == 200
        data = response.get_json()
        assert 'historical_data' in data
        assert isinstance(data['historical_data'], list)

class TestErrorHandling:
    def test_invalid_stock_symbol(self, client, auth_headers):
        """Test handling invalid stock symbol"""
        response = client.post('/api/stocks/buy',
            json={
                'symbol': 'INVALID',
                'quantity': 1
            },
            headers=auth_headers
        )
        
        assert response.status_code == 400
        assert 'Invalid stock symbol' in response.get_json()['error']

    def test_invalid_quantity(self, client, auth_headers):
        """Test handling invalid quantity"""
        response = client.post('/api/stocks/buy',
            json={
                'symbol': 'AAPL',
                'quantity': -1
            },
            headers=auth_headers
        )
        
        assert response.status_code == 400
        assert 'Invalid quantity' in response.get_json()['error']

    def test_missing_authentication(self, client):
        """Test requests without authentication"""
        response = client.get('/api/stocks/portfolio')
        
        assert response.status_code == 401
        assert 'Missing authentication token' in response.get_json()['error']
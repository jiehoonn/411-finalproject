import pytest
from flask import Flask, jsonify
from unittest.mock import MagicMock
from backend.routes.stocks import bp, AlphaVantageService, PortfolioService

# flask app instance for testing
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    return app

# setting up test client
@pytest.fixture
def client(app):
    return app.test_client()

# mock the alpha vantages ervice
@pytest.fixture
def mock_alpha_vantage():
    mock = MagicMock(AlphaVantageService)

    mock.get_stock_quote.return_value = {
        "Global Quote": {"05. price": "150.00"}
    }

    mock.get_time_series_daily.return_value = {
        "Time Series (Daily)": {
            "2024-12-06": {"4. close": "150.00"},
            "2024-12-05": {"4. close": "148.00"},
            "2024-12-04": {"4. close": "145.00"},
            "2024-12-03": {"4. close": "140.00"},
            "2024-12-02": {"4. close": "135.00"},
            "2024-12-01": {"4. close": "130.00"},
            "2024-11-30": {"4. close": "125.00"},
            "2024-11-29": {"4. close": "122.00"},
            "2024-11-28": {"4. close": "118.00"},
            "2024-11-27": {"4. close": "115.00"},
            "2024-11-26": {"4. close": "112.00"},
            "2024-11-25": {"4. close": "110.00"},
            "2024-11-24": {"4. close": "107.00"},
            "2024-11-23": {"4. close": "105.00"},
            "2024-11-22": {"4. close": "103.00"},
            "2024-11-21": {"4. close": "102.00"},
            "2024-11-20": {"4. close": "101.00"},
            "2024-11-19": {"4. close": "100.00"},
            "2024-11-18": {"4. close": "99.00"},
            "2024-11-17": {"4. close": "98.00"},
            "2024-11-16": {"4. close": "97.00"},
            "2024-11-15": {"4. close": "96.00"},
            "2024-11-14": {"4. close": "95.00"},
            "2024-11-13": {"4. close": "94.00"},
            "2024-11-12": {"4. close": "93.00"},
            "2024-11-11": {"4. close": "92.00"},
            "2024-11-10": {"4. close": "91.00"},
            "2024-11-09": {"4. close": "90.00"},
            "2024-11-08": {"4. close": "89.00"},
            "2024-11-07": {"4. close": "88.00"}
        }
    }

    mock.get_market_status.return_value = {
        "market_status": [
            {
                "market_type": "Stock Market",
                "region": "US",
                "primary_exchanges": ["NASDAQ", "NYSE"],
                "local_open": "09:30",
                "local_close": "16:00",
                "current_status": "Closed"
            }
        ]
    }
    return mock

# mock the portfolio service
@pytest.fixture
def mock_portfolio():
    mock = MagicMock(PortfolioService)
    return mock

# test for /api/stock/quote/<symbol>
def test_get_quote(client, mock_alpha_vantage):
    # Mock the service for the test
    symbol = "AAPL"
    response = client.get(f'/api/stock/quote/{symbol}')

    # verify the mock was called and response
    mock_alpha_vantage.get_stock_quote.assert_called_once_with(symbol)
    assert response.status_code == 200
    assert b"150.00" in response.data

    # test with invalid symbol
    mock_alpha_vantage.get_stock_quote.return_value = {"Global Quote": None}
    response = client.get(f'/api/stock/quote/{symbol}')
    assert response.status_code == 500
    assert b"error" in response.data


# test for /api/stock/value/<symbol>/<int:shares>
def test_calculate_value(client, mock_alpha_vantage):
    symbol = "AAPL"
    shares = 10
    response = client.get(f'/api/stock/value/{symbol}/{shares}')

    # verify the value calculation (150.00 * 10 = 1500.00)
    assert response.status_code == 200
    assert b'"value": 1500.0' in response.data

    # test with invalid symbol
    mock_alpha_vantage.get_stock_quote.return_value = {"Global Quote": None}
    response = client.get(f'/api/stock/value/{symbol}/{shares}')
    assert response.status_code == 500
    assert b"error" in response.data


# test for /lookup-stock
def test_lookup_stock(client, mock_alpha_vantage):
    # test with valid symbol
    symbol = "AAPL"
    response = client.get(f'/lookup-stock?symbol={symbol}')
    assert response.status_code == 200
    assert b"current_price" in response.data
    assert b"AAPL" in response.data

    # test with no symbol
    response = client.get('/lookup-stock?symbol=')
    assert response.status_code == 400
    assert b"No symbol given.." in response.data

    # test with invalid symbol (no data returned)
    mock_alpha_vantage.get_stock_quote.return_value = {"Global Quote": None}
    response = client.get(f'/lookup-stock?symbol={symbol}')
    assert response.status_code == 404
    assert b"No data found for the given symbol" in response.data

    # test with no market status for valid symbol
    response = client.get(f'/lookup-stock?symbol={symbol}')
    assert response.status_code == 200
    assert b"market_status" in response.data
    assert b"[]" in response.data



# test for /historical-data
def test_historical_data(client, mock_alpha_vantage):
    # test with valid symbol and range
    symbol = "AAPL"
    response = client.get(f'/historical-data?symbol={symbol}&range=1m')
    assert response.status_code == 200
    assert b"date" in response.data
    assert b"close" in response.data

    # test with no symbol
    response = client.get('/historical-data')
    assert response.status_code == 400
    assert b"Stock name required" in response.data

    # test with invalid symbol
    response = client.get('/lookup-stock?symbol=AAPLT')
    assert response.status_code == 404
    assert b"No historical data found for given symbol" in response.data

    # test with invalid range
    response = client.get(f'/historical-data?symbol={symbol}&range=invalid')
    assert response.status_code == 500
    assert b"Invalid data retrieved!" in response.data

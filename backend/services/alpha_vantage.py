from flask import current_app
import requests
import os

class AlphaVantageService:
    def __init__(self):
        self.api_key = os.getenv('ALPHA_VANTAGE_API_KEY') # Temporarily use os.getenv() instead of current_app
        self.base_url = 'https://www.alphavantage.co/query'

    def get_stock_quote(self, symbol):
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol,
            'apikey': self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json()

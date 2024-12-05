# Stock Trading Application

A powerful stock trading platform that enables individual investors to manage portfolios, execute trades, and monitor market conditions using the Alpha Vantage API.

## Features

### 1. View My Portfolio

- Display current stock holdings
- Show quantity and current price of each stock
- Calculate total value of each holding
- Display overall portfolio value
- **API Endpoints Used**: Quote Endpoint (fields: stock symbol, latest stock price, closing price)

### 2. Buy Stock

- Purchase shares with specified stock symbol and quantity
- Real-time market price execution
- **API Endpoints Used**: Quote Endpoint (fields: symbol, price, latest trading day, previous close)

### 3. Sell Stock

- Sell shares from current holdings
- Real-time market price execution
- **API Endpoints Used**: Quote Endpoint (fields: symbol, price, latest trading day)

### 4. Look Up Stock

- Detailed stock information
- Current market price
- Historical price data
- Company information
- **API Endpoints Used**: Quote and Time Series Daily Endpoint

### 5. Calculate Portfolio Value

- Real-time portfolio valuation
- Integration of the latest stock prices

## Technical Implementation

### Core Features and Routes

#### User Account Management

- **Routes**: `/create-account`, `/login`, `/update-password`
- Secure password storage with hashing
- Input validation
- SQLite database storage

#### Portfolio Management

- **Route**: `/portfolio`
- Live stock data integration
- Dynamic portfolio calculations

#### Trading Operations

- **Routes**: `/buy-stock`, `/sell-stock`
- Real-time price fetching
- Transaction validation
- Virtual wallet management

#### Stock Information

- **Route**: `/lookup-stock`
- Detailed stock data
- Caching implementation
- Historical data visualization

#### Analytics

- **Route**: `/historical-data`
- Visual data representation
- Customizable date ranges
- **API Endpoints Used**: Time Series Daily, Monthly, and Weekly Endpoints

## Initial Setup for Team Members

1. **Clone the repository:**

   ```bash
   git clone [your-repository-url]
   ```

2. **Navigate to the project directory:**

   ```bash
   cd [project-name]
   ```

3. **Install frontend dependencies:**

   ```bash
   cd frontend
   npm install
   ```

4. **Activate the virtual environment:**

   ```bash
   cd ../app/backend
   source venv/bin/activate
   ```

5. **Install backend dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Create a `.env` file in the backend directory:**

   ```bash
   echo "ALPHA_VANTAGE_API_KEY=your_api_key_here" > .env
   ```

   _Replace `your_api_key_here` with your actual Alpha Vantage API key._

## Running the Application

You will need two terminal windows to run the application.

### Terminal 1 - Frontend:

```bash
cd frontend
npm start
```

### Terminal 2 - Backend:

```bash
cd backend
flask run
```

## API Documentation

- [Alpha Vantage API Documentation](https://www.alphavantage.co/documentation/)
- Key endpoints used: Quote, Time Series Daily, ...
- Database: SQLAlchemy for data persistence.

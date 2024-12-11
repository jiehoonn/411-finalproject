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
- **API Endpoints Used**: Quote, Global Market Open & Close Status and Time Series Daily Endpoint

### 5. Stock Trends (Historical Data)

- Stock trends from the past 1 day, 10 days, 1 month, 6 month and 1 year
- **API Endpoints Used**: Time Series Daily, Time Series Intraday and Time Series Monthly Endpoint

### 6. Calculate Portfolio Value

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


## Route Documentation

### 1. Create Account

- **Route**: `/create-account`  
- **Request Type**: POST  
- **Purpose**: Creates a new user account with a username and password.  

#### Request Body:
```json
{
  "username": "newuser123",
  "password": "securepassword"
}
```

#### Response Format:
**Success Response:**
```json
{
  "message": "Account created successfully",
  "status": "200"
}
```

---

### 2. Login

- **Route**: `/login`  
- **Request Type**: POST  
- **Purpose**: Authenticates an existing user with their username and password.  

#### Request Body:
```json
{
  "username": "existinguser",
  "password": "userpassword"
}
```

#### Response Format:
**Success Response:**
```json
{
  "message": "Login successful",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
  "status": "200"
}
```

**Error Response:**
```json
{
  "message": "Invalid credentials",
  "status": "401"
}
```

---

### 3. Update Password

- **Route**: `/update-password`  
- **Request Type**: POST  
- **Purpose**: Allows a user to update their password.  

#### Request Body:
```json
{
  "username": "existinguser",
  "old_password": "oldpassword",
  "new_password": "newsecurepassword"
}
```

#### Response Format:
**Success Response:**
```json
{
  "message": "Password updated successfully",
  "status": "200"
}
```

**Error Response:**
```json
{
  "message": "Invalid credentials",
  "status": "401"
}
```

---

### 4. Portfolio Overview

- **Route**: `/portfolio`  
- **Request Type**: GET  
- **Purpose**: Retrieves the user's current portfolio, including holdings and their values.  

#### Response Format:
**Success Response:**
```json
{
  "portfolio": [
    {
      "symbol": "AAPL",
      "quantity": 10,
      "price": 150.50,
      "total_value": 1505.00
    },
    {
      "symbol": "GOOG",
      "quantity": 5,
      "price": 2800.00,
      "total_value": 14000.00
    }
  ],
  "total_portfolio_value": 15505.00,
  "status": "200"
}
```

---

### 5. Buy Stock

- **Route**: `/buy-stock`  
- **Request Type**: POST  
- **Purpose**: Allows the user to purchase a specified quantity of a stock.  

#### Request Body:
```json
{
  "symbol": "AAPL",
  "quantity": 5
}
```

#### Response Format:
**Success Response:**
```json
{
  "message": "Stock purchased successfully",
  "status": "200"
}
```

**Error Response:**
```json
{
  "message": "Insufficient funds",
  "status": "400"
}
```

---

### 6. Sell Stock

- **Route**: `/sell-stock`  
- **Request Type**: POST  
- **Purpose**: Allows the user to sell a specified quantity of a stock.  

#### Request Body:
```json
{
  "symbol": "AAPL",
  "quantity": 5
}
```

#### Response Format:
**Success Response:**
```json
{
  "message": "Stock sold successfully",
  "status": "200"
}
```

**Error Response:**
```json
{
  "message": "Insufficient stock quantity",
  "status": "400"
}
```

---

### 7. Lookup Stock

- **Route**: `/lookup-stock`  
- **Request Type**: GET  
- **Purpose**: Retrieves detailed information about a specific stock.  

#### Query Parameters:
- `symbol` (String): Stock symbol to look up.

#### Response Format:
**Success Response:**
```json
{
  "symbol": "AAPL",
  "price": 150.50,
  "open": 148.00,
  "close": 149.50,
  "high": 151.00,
  "low": 147.50,
  "status": "200"
}
```

---

### 8. Historical Data

- **Route**: `/historical-data`  
- **Request Type**: GET  
- **Purpose**: Retrieves historical data for a stock over a specified period.  

#### Query Parameters:
- `symbol` (String): Stock symbol.
- `range` (String): Time range (e.g., `1d`, `10d`, `1m`, `6m`, `1y`).

#### Response Format:
**Success Response:**
```json
{
  "symbol": "AAPL",
  "historical_data": [
    { "date": "2024-12-01", "close": 150.50 },
    { "date": "2024-12-02", "close": 149.50 }
  ],
  "status": "200"
}

```

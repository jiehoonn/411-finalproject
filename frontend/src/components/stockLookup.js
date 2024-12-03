import React, { useState } from 'react';

const StockLookup = () => {
    const [symbol, setSymbol] = useState('');
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);

    const getData = async () => {
        setError(null);
        try {
            const response = await fetch(`http://127.0.0.1:5000/lookup-stock?symbol=${symbol}`);
            if (!response.ok) throw new Error("Failed to fetch stock data");
            const result = await response.json();
            setData(result);
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div>
            <h2>Stock Lookup</h2>
            <input
                type="text"
                placeholder="Enter symbol"
                value={symbol}
                onChange={(e) => setSymbol(e.target.value)}
            />
            <button onClick={getData}>Lookup</button>

            {error && <p style={{ color: 'red' }}>{error}</p>}

            {data && (
                <div>
                    <h3>{data.symbol}</h3>
                    <p>Current Price: ${data.current_price}</p>
                    <p>Volume: {data.volume}</p>
                    <h4>Last 7 Days</h4>
                    <ul>
                        {data.last_7_days.map((day) => (
                            <li key={day.date}>{day.date}: ${day.close}</li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default StockLookup;

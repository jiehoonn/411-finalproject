import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Portfolio = () => {
    const [portfolioData, setPortfolioData] = useState(null);
    const [balance, setBalance] = useState(0);
    const navigate = useNavigate();

    useEffect(() => {
        fetchPortfolioData();
    }, []);

    const fetchPortfolioData = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/dashboard/portfolio-summary', {
                credentials: 'include'
            });
            if (response.ok) {
                const data = await response.json();
                setPortfolioData(data);
                setBalance(data.cash_balance);
            }
        } catch (error) {
            console.error('Error fetching portfolio:', error);
        }
    };

    const handleViewDashboard = () => {
        navigate('/dashboard');
    };

    return (
        <div style={{ padding: '20px' }}>
            <h1>Your Portfolio</h1>
            
            <div style={{ 
                backgroundColor: '#f0f2f5',
                padding: '20px',
                borderRadius: '8px',
                marginBottom: '20px'
            }}>
                <h2>Account Overview</h2>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <div>
                        <h3>Available Cash</h3>
                        <p style={{ fontSize: '24px', color: '#52c41a' }}>
                            ${balance.toLocaleString()}
                        </p>
                    </div>
                    <div>
                        <h3>Portfolio Value</h3>
                        <p style={{ fontSize: '24px', color: '#1890ff' }}>
                            ${portfolioData?.portfolio_value.toLocaleString()}
                        </p>
                    </div>
                    <div>
                        <h3>Total Value</h3>
                        <p style={{ fontSize: '24px', color: '#722ed1' }}>
                            ${portfolioData?.total_value.toLocaleString()}
                        </p>
                    </div>
                </div>
            </div>

            <div style={{ marginBottom: '20px' }}>
                {portfolioData?.stocks.map((stock) => (
                    <div key={stock.symbol} style={{
                        border: '1px solid #ccc',
                        borderRadius: '8px',
                        padding: '15px',
                        marginBottom: '10px'
                    }}>
                        <h3>{stock.symbol}</h3>
                        <p>Shares Owned: {stock.shares}</p>
                        <p>Current Value: ${stock.current_value.toLocaleString()}</p>
                        <p>Purchase Price: ${stock.purchase_price}</p>
                        <p>Total Return: ${(stock.current_value - (stock.purchase_price * stock.shares)).toLocaleString()}</p>
                    </div>
                ))}
            </div>

            <button 
                onClick={handleViewDashboard}
                style={{
                    padding: '10px 20px',
                    backgroundColor: '#007BFF',
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer'
                }}
            >
                Go to Trading Dashboard
            </button>
        </div>
    );
};

export default Portfolio;

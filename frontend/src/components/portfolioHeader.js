import React from 'react';
import { Card, Typography } from 'antd';

const { Text } = Typography;

function PortfolioHeader({ balance, portfolioValue }) {
    // const [balance, setBalance] = useState(0);
    // const [portfolioValue, setPortfolioValue] = useState(0);

    // useEffect(() => {
    //     fetchBalanceAndPortfolio();
    //     const interval = setInterval(fetchBalanceAndPortfolio, 60000);
    //     return () => clearInterval(interval);
    // }, []);

    // const fetchBalanceAndPortfolio = async () => {
    //     const response = await fetch('http://127.0.0.1:5000/api/portfolio-status');
    //     const data = await response.json();
    //     setBalance(data.balance);
    //     setPortfolioValue(data.portfolio_value);
    // };

    return (
        <Card style={{ marginBottom: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <Text strong>Balance: ${balance.toLocaleString()}</Text>
                <Text strong>Portfolio Value: ${portfolioValue.toLocaleString()}</Text>
            </div>
        </Card>
    );
}

export default PortfolioHeader;

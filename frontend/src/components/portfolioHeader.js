import React, { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
import { Card, Typography, Button } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';

const { Text } = Typography;

const PortfolioHeader = forwardRef((props, ref) => {
    const [balance, setBalance] = useState(0);
    const [portfolioValue, setPortfolioValue] = useState(0);
    const [isLoading, setIsLoading] = useState(false);

    const fetchBalanceAndPortfolio = async () => {
        setIsLoading(true);
        try {
            const user = JSON.parse(localStorage.getItem('user'));
            const response = await fetch(`http://127.0.0.1:5000/api/portfolio-status/${user.id}`);
            const data = await response.json();
            setBalance(data.balance);
            setPortfolioValue(data.portfolio_value);
        } catch (error) {
            console.error('Error fetching portfolio data:', error);
        } finally {
            setIsLoading(false);
        }
    };

    // Expose fetchBalanceAndPortfolio to parent components through ref
    useImperativeHandle(ref, () => ({
        fetchBalanceAndPortfolio
    }));

    // Immediately fetch value upon log in.
    useEffect(() => {
        fetchBalanceAndPortfolio();
    }, []);

    return (
        <Card style={{ marginBottom: '20px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                    <Text strong>Balance: ${balance.toLocaleString()}</Text>
                    <Text strong style={{ marginLeft: '20px' }}>Portfolio Value: ${portfolioValue.toLocaleString()}</Text>
                </div>
                <Button 
                    icon={<ReloadOutlined />} 
                    onClick={fetchBalanceAndPortfolio}
                    loading={isLoading}
                >
                    Refresh
                </Button>
            </div>
        </Card>
    );
});

export default PortfolioHeader;
import React, { useState, useEffect } from "react";
import { Layout, Card, Typography, Row, Col, Select, Input, Button } from "antd";
import { useNavigate } from 'react-router-dom';
import HistoricalData from "../components/historicalData";
import StockLookup from "../components/stockLookup";
import BuyStock from "../components/buyStock";
import SellStock from "../components/sellStock";

const { Title, Text } = Typography;
const { Header, Content } = Layout;
const { Option } = Select;

function Dashboard() {
    const [range, setRange] = useState("1d");
    const [shares, setShares] = useState('');
    const [amount, setAmount] = useState('');
    const [tradeType, setTradeType] = useState('shares');
    const [userBalance, setUserBalance] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        fetchUserBalance();
    }, []);

    const fetchUserBalance = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/dashboard/balance', {
                credentials: 'include'
            });
            const data = await response.json();
            setUserBalance(data.balance);
        } catch (error) {
            console.error('Error fetching balance:', error);
        }
    };

    const handleTrade = async (symbol, action) => {
        const tradeData = {
            symbol,
            action,
            [tradeType]: tradeType === 'shares' ? parseFloat(shares) : parseFloat(amount)
        };

        try {
            const response = await fetch('http://127.0.0.1:5000/trade', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify(tradeData)
            });

            if (response.ok) {
                setShares('');
                setAmount('');
                fetchUserBalance();
            }
        } catch (error) {
            console.error('Trade failed:', error);
        }
    };

    return (
        <Layout>
            <Header>
                <Title level={2} style={{ color: "white", textAlign: "center", margin: 10 }}>
                    Stock Trading Platform
                </Title>
                <Button 
                    onClick={() => navigate('/portfolio')}
                    style={{
                        position: 'absolute',
                        right: '20px',
                        top: '20px'
                    }}
                >
                    View Portfolio
                </Button>
            </Header>
            <Content style={{ padding: "50px" }}>
                <Card style={{ marginBottom: '20px' }}>
                    <Title level={4}>Available Trading Balance</Title>
                    <Text style={{ fontSize: '24px', color: '#52c41a' }}>
                        ${userBalance?.toLocaleString()}
                    </Text>
                </Card>

                <Row gutter={[20, 20]}>
                    <Col xs={24} sm={12} lg={12}>
                        <StockLookup />
                    </Col>

                    <Col xs={24} sm={12} lg={12}>
                        <HistoricalData range={range} />
                    </Col>

                    <Col xs={24} sm={12} lg={12}>
                        <Card title="Trade Stock" bordered>
                            <Select 
                                value={tradeType} 
                                onChange={(value) => setTradeType(value)}
                                style={{ width: '100%', marginBottom: '10px' }}
                            >
                                <Option value="shares">Trade by Shares</Option>
                                <Option value="amount">Trade by Dollar Amount</Option>
                            </Select>
                            
                            {tradeType === 'shares' ? (
                                <Input
                                    type="number"
                                    value={shares}
                                    onChange={(e) => setShares(e.target.value)}
                                    placeholder="Number of shares"
                                    step="0.01"
                                    style={{ marginBottom: '10px' }}
                                />
                            ) : (
                                <Input
                                    type="number"
                                    value={amount}
                                    onChange={(e) => setAmount(e.target.value)}
                                    placeholder="Dollar amount"
                                    step="0.01"
                                    style={{ marginBottom: '10px' }}
                                />
                            )}
                            
                            <Row gutter={[10, 10]}>
                                <Col span={12}>
                                    <BuyStock onBuy={handleTrade} />
                                </Col>
                                <Col span={12}>
                                    <SellStock onSell={handleTrade} />
                                </Col>
                            </Row>
                        </Card>
                    </Col>
                </Row>
            </Content>
        </Layout>
    );
}

export default Dashboard;

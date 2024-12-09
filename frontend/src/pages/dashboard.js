import React, { useState } from "react";
import { Layout, Card, Typography, Row, Col } from "antd";
import HistoricalData from "../components/historicalData";
import StockLookup from "../components/stockLookup";
import BuyStock from "../components/buyStock";
import SellStock from "../components/sellStock";
import PortfolioHeader from "../components/portfolioHeader";

const { Title } = Typography;
const { Header, Content } = Layout;

function Dashboard() {
  const [balance, setBalance] = useState(0);
  const [portfolioValue, setPortfolioValue] = useState(0);

  const fetchBalanceAndPortfolio = async () => {
    const response = await fetch('http://127.0.0.1:5000/api/portfolio-status');
    const data = await response.json();
    setBalance(data.balance);
    setPortfolioValue(data.portfolio_value);
  };

  const [range, setRange] = useState("1d");
  return (
    <Layout>
      <Header>
        <Title level={2} style={{ color: "white", textAlign: "center", margin: 10 }}>
          Stock Trading Platform
        </Title>
      </Header>
      <Content style={{ padding: "50px" }}>
        <PortfolioHeader balance={balance} portfolioValue={portfolioValue}/>
        <Row gutter={[20, 20]}>
          <Col xs={24} sm={12} lg={12}>
            <StockLookup />
          </Col>

          <Col xs={24} sm={12} lg={12}>
            <HistoricalData range={range} />
          </Col>

          <Col xs={24} sm={12} lg={12}>
            <Card title="Buy Stock" bordered>
              <BuyStock fetchBalanceAndPortfolio={fetchBalanceAndPortfolio}/>
            </Card>
          </Col>

          <Col xs={24} sm={12} lg={12}>
            <Card title="Sell Stock" bordered>
              <SellStock fetchBalanceAndPortfolio={fetchBalanceAndPortfolio}/>
            </Card>
          </Col>
        </Row>
      </Content>
    </Layout>
  );
}

export default Dashboard;

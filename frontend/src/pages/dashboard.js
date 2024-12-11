import React, { useRef } from "react";
import { Layout, Card, Typography, Row, Col } from "antd";
import HistoricalData from "../components/historicalData";
import StockLookup from "../components/stockLookup";
import BuyStock from "../components/buyStock";
import SellStock from "../components/sellStock";
import PortfolioHeader from "../components/portfolioHeader";

const { Title } = Typography;
const { Header, Content } = Layout;

function Dashboard() {
  const portfolioHeaderRef = useRef();

  return (
    <Layout>
      <Header>
        <Title level={2} style={{ color: "white", textAlign: "center", margin: 10 }}>
          Stock Trading Platform
        </Title>
      </Header>
      <Content style={{ padding: "50px" }}>
        <PortfolioHeader ref={portfolioHeaderRef} />
        <Row gutter={[20, 20]}>
          <Col xs={24} sm={12} lg={12}>
            <StockLookup />
          </Col>

          <Col xs={24} sm={12} lg={12}>
            <HistoricalData />
          </Col>

          <Col xs={24} sm={12} lg={12}>
            <Card title="Buy Stock" bordered>
              <BuyStock onSuccess={() => portfolioHeaderRef.current?.fetchBalanceAndPortfolio()} />
            </Card>
          </Col>

          <Col xs={24} sm={12} lg={12}>
            <Card title="Sell Stock" bordered>
              <SellStock onSuccess={() => portfolioHeaderRef.current?.fetchBalanceAndPortfolio()} />
            </Card>
          </Col>
        </Row>
      </Content>
    </Layout>
  );
}

export default Dashboard;
import React, { useState } from "react";
import { Card, Input, Button, List, Typography, Alert } from "antd";

const { Title, Text } = Typography;

const StockLookup = () => {
  const [symbol, setSymbol] = useState("");
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  const getData = async () => {
    setError(null);
    setData(null);
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
    <Card title="Stock Lookup" bordered={true} style={{ marginBottom: 20 }}>
      <Input
        placeholder="Enter stock symbol (e.g., AAPL)"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        style={{ marginBottom: 16 }}
      />
      <Button type="primary" onClick={getData} block disabled={!symbol}>
        Lookup
      </Button>

      {error && (
        <Alert message="Error" description={error} type="error" showIcon style={{ marginTop: 16 }} />
      )}

      {data && (
        <div style={{ marginTop: 16 }}>
          <Title level={4}>{data.symbol}</Title>
          <Text>Current Price: ${data.current_price}</Text>
          <br />
          <Text>Volume: {data.volume}</Text>

          <Title level={5} style={{ marginTop: 16 }}>
            Last 7 Days
          </Title>
          <List
            dataSource={data.last_7_days}
            renderItem={(day) => (
              <List.Item>
                {day.date}: <Text strong>${day.close}</Text>
              </List.Item>
            )}
          />

          <Title level={5} style={{ marginTop: 16 }}>
            Market Status
          </Title>
          {data.market_status && data.market_status.length > 0 ? (
            <List
              dataSource={data.market_status}
              renderItem={(market) => (
                <List.Item>
                  <Text strong>{market.region} - {market.market_type}</Text><br />
                  <Text>Exchanges: {market.primary_exchanges}</Text><br />
                  <Text>Open: {market.local_open} - Close: {market.local_close}</Text><br />
                  <Text>Status: {market.current_status}</Text>
                </List.Item>
              )}
            />
          ) : (
            <Text>No market status data available</Text>
          )}
        </div>
      )}
    </Card>
  );
};

export default StockLookup;

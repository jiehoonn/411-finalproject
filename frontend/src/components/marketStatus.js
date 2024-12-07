import React, { useEffect, useState } from "react";
import { Card, Alert, Table } from "antd";

const MarketStatus = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [marketStatus, setMarketStatus] = useState([]);

  useEffect(() => {
    const fetchMarketStatus = async () => {
      setLoading(true);
      try {
        const response = await fetch("http://127.0.0.1:5000/market-status");
        if (!response.ok) throw new Error("Failed to fetch market status");
        const data = await response.json();
        setMarketStatus(data.markets || []);
      } catch (err) {
        setError(err.message);
      }
      setLoading(false);
    };

    fetchMarketStatus();
  }, []);

  const columns = [
    {
      title: "Region",
      dataIndex: "region",
      key: "region",
    },
    {
      title: "Market Type",
      dataIndex: "market_type",
      key: "market_type",
    },
    {
      title: "Current Status",
      dataIndex: "current_status",
      key: "current_status",
      render: (status) => (
        <span style={{ color: status === "open" ? "green" : "red" }}>
          {status.charAt(0).toUpperCase() + status.slice(1)}
        </span>
      ),
    },
    {
      title: "Local Open",
      dataIndex: "local_open",
      key: "local_open",
    },
    {
      title: "Local Close",
      dataIndex: "local_close",
      key: "local_close",
    }
  ];

  if (loading) {
    return (
      <div style={{ height: "100vh", display: "flex", justifyContent: "center", alignItems: "center" }}>
        <div>Loading...</div>
      </div>
    );
  }

  if (error) {
    return <Alert message="Error" description={error} type="error" showIcon />;
  }

  return (
    <Card title="Market Status">
      <Table
        columns={columns}
        dataSource={marketStatus}
        rowKey={(record) => `${record.region}-${record.market_type}`}
        pagination={false}
        size="small"
      />
    </Card>
  );
};

export default MarketStatus;

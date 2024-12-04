import React, { useState } from "react";
import { Card, Button, Radio, Alert, Input } from "antd";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);


const HistoricalData = () => {
  const [symbol, setSymbol] = useState("");
  const [range, setRange] = useState("1d");
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch(`http://127.0.0.1:5000/historical-data?symbol=${symbol}&range=${range}`);
      if (!response.ok) throw new Error("Failed to fetch historical data");
      const data = await response.json();
      const labels = data.map((entry) => entry.date);
      const closePrices = data.map((entry) => entry.close);

      setChartData({
        labels,
        datasets: [
          {
            label: `Stock Price (${symbol})`,
            data: closePrices,
            fill: false,
            borderColor: "rgb(191,52,52)",
            tension: 0.1,
          },
        ],
      });
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const handleRangeChange = (e) => {
    setRange(e.target.value);
  };

  return (
    <Card title="Historical Data" bordered={true}>
      <Input
        placeholder="Enter stock symbol (e.g., AAPL)"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        style={{ marginBottom: 16 }}
      />

      <Radio.Group
        onChange={handleRangeChange}
        value={range}
        style={{ display: "block", marginBottom: 16 }}
        buttonStyle="solid"
      >
        <Radio.Button value="1d">1D</Radio.Button>
        <Radio.Button value="10d">10D</Radio.Button>
        <Radio.Button value="1m">1M</Radio.Button>
        <Radio.Button value="6m">6M</Radio.Button>
        <Radio.Button value="1y">1Y</Radio.Button>
      </Radio.Group>

      <Button type="primary" onClick={fetchData} block disabled={!symbol || loading}>
        {loading ? "Loading..." : "Fetch Data"}
      </Button>

      {error && (
        <Alert message="Error" description={error} type="error" showIcon style={{ marginTop: 16 }} />
      )}

      {chartData && (
        <div style={{ marginTop: 16, height: 400 }}>
          <Line
            data={chartData}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              plugins: {
                legend: {
                  position: "top",
                },
              },
              scales: {
                x: {
                  ticks: {
                    maxRotation: 90,
                    minRotation: 45,
                  },
                },
              },
            }}
          />
        </div>
      )}
    </Card>
  );
};

export default HistoricalData;

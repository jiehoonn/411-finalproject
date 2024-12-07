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
  const [symbols, setSymbols] = useState([""]);
  const [range, setRange] = useState("1d");
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const datasets = [];
      for (const symbol of symbols) {
        if (!symbol) continue; // Skip empty symbols
        const response = await fetch(`http://127.0.0.1:5000/historical-data?symbol=${symbol}&range=${range}`);
        if (!response.ok) throw new Error(`Failed to fetch data for ${symbol}`);
        const data = await response.json();
        const labels = data.map((entry) => entry.date);
        const closePrices = data.map((entry) => entry.close);

        datasets.push({
          label: `Stock Price (${symbol})`,
          data: closePrices,
          fill: false,
          borderColor: `hsl(${Math.random() * 360}, 70%, 50%)`, // Random color
          tension: 0.1,
        });

        // Set labels only once
        if (!chartData?.labels) {
          setChartData({
            labels,
            datasets: [],
          });
        }
      }

      setChartData((prev) => ({
        ...prev,
        datasets,
      }));
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  const handleRangeChange = (e) => {
    setRange(e.target.value);
  };

  const handleSymbolChange = (index, value) => {
    const updatedSymbols = [...symbols];
    updatedSymbols[index] = value;
    setSymbols(updatedSymbols);
  };

  const addSymbol = () => {
    if (symbols.length < 3) setSymbols([...symbols, ""]);
  };

  const removeSymbol = (index) => {
    if (symbols.length > 1) {
      setSymbols(symbols.filter((_, i) => i !== index));
    }
  };

  return (
    <Card title="Historical Data" bordered={true}>
      {symbols.map((symbol, index) => (
        <div key={index} style={{ display: "flex", alignItems: "center", marginBottom: 8 }}>
          <Input
            placeholder={`Enter stock symbol (e.g., AAPL)`}
            value={symbol}
            onChange={(e) => handleSymbolChange(index, e.target.value)}
            style={{ flex: 1, marginRight: 8 }}
          />
          <Button
            danger
            onClick={() => removeSymbol(index)}
            disabled={symbols.length === 1} // Prevent removing the last symbol
          >
            Remove
          </Button>
        </div>
      ))}

      <Button type="dashed" onClick={addSymbol} block style={{ marginBottom: 16 }} disabled={symbols.length >= 3}>
        Add Symbol
      </Button>

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

      <Button type="primary" onClick={fetchData} block disabled={loading || symbols.every((symbol) => !symbol)}>
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

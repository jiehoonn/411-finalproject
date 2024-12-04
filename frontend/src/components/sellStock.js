import React from "react";
import { Form, Input, Button } from "antd";

function SellStock() {
  return (
    <Form layout="vertical">
      <Form.Item label=" Symbol" name="symbol">
        <Input placeholder="Enter symbol" />
      </Form.Item>
      <Form.Item label="Quantity" name="quantity">
        <Input type="number" placeholder="Enter quantity" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" danger>
          Sell
        </Button>
      </Form.Item>
    </Form>
  );
}

export default SellStock;

import React from "react";
import { Form, Input, Button, message } from "antd";

function BuyStock({ fetchBalanceAndPortfolio }) {
  const [form] = Form.useForm();

  const onFinish = async (values) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/buy-stock', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(values),
      });
      const data = await response.json();

      if (data.success) {
        message.success('Stock purchased successfully');
        form.resetFields();
        fetchBalanceAndPortfolio();
      } else {
        message.error(data.error);
      }
    } catch (error) {
      message.error('Failed to purchase stock');
    }
  };

  return (
    <Form form={form} layout="vertical" onFinish={onFinish}>
      <Form.Item label="Symbol" name="symbol" rules={[{ required: true }]}>
        <Input placeholder="Enter symbol" />
      </Form.Item>
      <Form.Item label="Quantity" name="quantity" rules={[{ required: true }]}>
        <Input type="number" placeholder="Enter quantity" />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit">Buy</Button>
      </Form.Item>
    </Form>
  );
}

export default BuyStock;

import React, { useState } from 'react';
import { Form, Input, Button, message, Card } from 'antd';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [form] = Form.useForm();
  const navigate = useNavigate();

  const onFinish = async (values) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(values),
      });

      const data = await response.json();

      if (response.ok) {
        message.success('Login successful');
        // Store user data in localStorage or state management system
        localStorage.setItem('user', JSON.stringify(data.user));
        navigate('/dashboard');
      } else {
        message.error(data.error || 'Login failed');
      }
    } catch (error) {
      message.error('An error occurred during login');
    }
  };

  return (
    <Card title="Login" style={{ maxWidth: 400, margin: '50px auto' }}>
      <Form form={form} layout="vertical" onFinish={onFinish}>
        <Form.Item 
          name="username" 
          label="Username"
          rules={[{ required: true, message: 'Please enter your username' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item 
          name="password" 
          label="Password"
          rules={[{ required: true, message: 'Please enter your password' }]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" block>
            Login
          </Button>
        </Form.Item>
      </Form>
        <Button type="link" onClick={() => navigate('/register')}>
            Don't have an account? Register here
        </Button>
    </Card>
  );
}

export default Login;
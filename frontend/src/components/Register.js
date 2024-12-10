import React, { useState } from 'react';
import { Form, Input, Button, message, Card } from 'antd';
import { useNavigate } from 'react-router-dom';

function Register() {
  const [form] = Form.useForm();
  const navigate = useNavigate();

  const onFinish = async (values) => {
    try {
      const response = await fetch('http://127.0.0.1:5000/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(values),
      });

      const data = await response.json();

      if (response.ok) {
        message.success('Registration successful');
        navigate('/login');
      } else {
        message.error(data.error || 'Registration failed');
      }
    } catch (error) {
      message.error('An error occurred during registration');
    }
  };

  return (
    <Card title="Register" style={{ maxWidth: 400, margin: '50px auto' }}>
      <Form form={form} layout="vertical" onFinish={onFinish}>
        <Form.Item 
          name="username" 
          label="Username"
          rules={[{ required: true, message: 'Please enter a username' }]}
        >
          <Input />
        </Form.Item>

        <Form.Item 
          name="email" 
          label="Email"
          rules={[
            { required: true, message: 'Please enter your email' },
            { type: 'email', message: 'Please enter a valid email' }
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item 
          name="password" 
          label="Password"
          rules={[{ required: true, message: 'Please enter a password' }]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" block>
            Register
          </Button>
        </Form.Item>
      </Form>
        <Button type="link" onClick={() => navigate('/login')}>
            Already have an account? Login here
        </Button>
    </Card>
  );
}

export default Register;
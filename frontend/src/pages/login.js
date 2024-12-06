import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from 'antd';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://127.0.0.1:5000/user/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                credentials: 'include',
                body: JSON.stringify({ username, password }),
            });

            if (response.ok) {
                navigate('/dashboard');
            } else {
                const data = await response.json();
                setMessage(data.error);
            }
        } catch (error) {
            setMessage('Login failed');
        }
    };

    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>Stock Trading Platform</h1>
            <form onSubmit={handleLogin} style={{ display: 'inline-block' }}>
                <div>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Username"
                        style={{ margin: '10px', padding: '5px' }}
                    />
                </div>
                <div>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                        style={{ margin: '10px', padding: '5px' }}
                    />
                </div>
                <Button type="primary" htmlType="submit">Login</Button>
                <Button onClick={() => navigate('/register')} style={{ marginLeft: '10px' }}>
                    Register New Account
                </Button>
            </form>
            {message && <p style={{ color: 'red' }}>{message}</p>}
        </div>
    );
};

export default Login;

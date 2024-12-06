import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from 'antd';

const Register = () => {
    const [username, setUsername] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [message, setMessage] = useState('');
    const navigate = useNavigate();

    const handleRegister = async (e) => {
        e.preventDefault();
        
        if (password !== confirmPassword) {
            setMessage('Passwords do not match');
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/user/create-account', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, email, password }),
            });

            if (response.ok) {
                navigate('/login');
            } else {
                const data = await response.json();
                setMessage(data.error);
            }
        } catch (error) {
            setMessage('Registration failed');
        }
    };

    return (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>
            <h1>Create New Account</h1>
            <form onSubmit={handleRegister} style={{ display: 'inline-block' }}>
                <div>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Username"
                        style={{ margin: '10px', padding: '5px' }}
                        required
                    />
                </div>
                <div>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Email"
                        style={{ margin: '10px', padding: '5px' }}
                        required
                    />
                </div>
                <div>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                        style={{ margin: '10px', padding: '5px' }}
                        required
                    />
                </div>
                <div>
                    <input
                        type="password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        placeholder="Confirm Password"
                        style={{ margin: '10px', padding: '5px' }}
                        required
                    />
                </div>
                <Button type="primary" htmlType="submit">Register</Button>
                <Button onClick={() => navigate('/login')} style={{ marginLeft: '10px' }}>
                    Back to Login
                </Button>
            </form>
            {message && <p style={{ color: 'red' }}>{message}</p>}
        </div>
    );
};

export default Register;

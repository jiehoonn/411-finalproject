import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

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

            const data = await response.json();
            
            if (response.ok) {
                setMessage('Login successful!');
                navigate('/dashboard');
            } else {
                setMessage(data.error);
            }
        } catch (error) {
            setMessage('An error occurred during login.');
        }
    };

    return (
        <div style={{ fontFamily: "Arial, sans-serif", textAlign: "center", marginTop: "50px" }}>
            <h2>Login</h2>
            <form onSubmit={handleLogin} style={{ display: "inline-block", textAlign: "left" }}>
                <div style={{ marginBottom: "10px" }}>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder="Username"
                        style={{
                            width: "200px",
                            padding: "8px",
                            marginBottom: "10px",
                            border: "1px solid #ccc",
                            borderRadius: "4px",
                        }}
                        required
                    />
                </div>
                <div style={{ marginBottom: "10px" }}>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Password"
                        style={{
                            width: "200px",
                            padding: "8px",
                            marginBottom: "10px",
                            border: "1px solid #ccc",
                            borderRadius: "4px",
                        }}
                        required
                    />
                </div>
                <button
                    type="submit"
                    style={{
                        width: "100%",
                        padding: "10px",
                        backgroundColor: "#007BFF",
                        color: "white",
                        border: "none",
                        borderRadius: "4px",
                        cursor: "pointer",
                    }}
                >
                    Login
                </button>
            </form>
            {message && (
                <p style={{ marginTop: "20px", color: message.includes('successful') ? 'green' : 'red' }}>
                    {message}
                </p>
            )}
        </div>
    );
};

export default Login;

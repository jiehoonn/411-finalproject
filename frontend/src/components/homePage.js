import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>Welcome to Stock Trading Application</h1>
      <button onClick={() => navigate('/login')} style={{ margin: '10px', padding: '10px', backgroundColor: 'blue', color: 'white' }}>
        Login
      </button>
      <button onClick={() => navigate('/register')} style={{ margin: '10px', padding: '10px', backgroundColor: 'green', color: 'white' }}>
        Register
      </button>
    </div>
  );
};

export default HomePage;

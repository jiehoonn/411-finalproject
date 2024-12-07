import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Dashboard from './pages/dashboard';
// import Portfolio from './pages/portfolio';
import RegisterPage from './components/userRegistration';
import LoginPage from './components/loginPage';
import MainPage from './components/mainPage';

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Navigate to="/main" />} />
                <Route path="/main" element={<MainPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/dashboard" element={<Dashboard />} />
                {/* <Route path="/portfolio" element={<Portfolio />} /> */}
            </Routes>
        </Router>
    );
}

export default App;

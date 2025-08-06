import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage.jsx';
import ChatPage from './pages/ChatPage.jsx';
import './index.css';

function App() {
    // The source of truth for our logged-in state is whether a token exists in storage.
    const [token, setToken] = useState(localStorage.getItem('supermaya_token'));

    const handleLogin = (newToken) => {
        localStorage.setItem('supermaya_token', newToken);
        setToken(newToken); // This triggers the re-render to the ChatPage
    };

    const handleLogout = () => {
        localStorage.removeItem('supermaya_token');
        setToken(null); // This triggers the re-render to the LoginPage
    };

    return (
        <Router>
            <Routes>
                <Route 
                    path="/" 
                    element={token ? <ChatPage onLogout={handleLogout} /> : <Navigate to="/login" />} 
                />
                <Route 
                    path="/login" 
                    element={!token ? <LoginPage onLogin={handleLogin} /> : <Navigate to="/" />} 
                />
            </Routes>
        </Router>
    );
}

export default App;
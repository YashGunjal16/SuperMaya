import React, { useState } from 'react';
import { login, register } from '../api';

export default function LoginPage({ onLogin }) {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [isRegistering, setIsRegistering] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        try {
            let response;
            if (isRegistering) {
                await register(email, password);
                // After registering, automatically log in
                response = await login(email, password);
            } else {
                response = await login(email, password);
            }
            onLogin(response.data.access_token);
        } catch (err) {
            setError(isRegistering ? 'Registration failed.' : 'Login failed. Invalid credentials.');
            console.error(err);
        }
    };

    return (
        <div className="login-container">
            <form onSubmit={handleSubmit} className="login-form">
                <h2>{isRegistering ? 'Register for SuperMaya' : 'SuperMaya AI Login'}</h2>
                <input type="email" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} required />
                <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} required />
                <button type="submit">{isRegistering ? 'Register & Login' : 'Login'}</button>
                {error && <p className="error-message">{error}</p>}
                <button type="button" className="toggle-auth" onClick={() => setIsRegistering(!isRegistering)}>
                    {isRegistering ? 'Already have an account? Login' : "Don't have an account? Register"}
                </button>
            </form>
        </div>
    );
}
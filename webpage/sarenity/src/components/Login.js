import React, { useState } from 'react';
import './Login.css';

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = () => {
    if (username === 'sarenity' && password === 'sar3n!ty25%') {
      onLogin(username, password);
    }
  };

  const handleUsernameChange = (e) => {
    const value = e.target.value;
    if (/^[a-zA-Z0-9!@#$%]*$/.test(value) && value.length <= 20) {
      setUsername(value);
    }
  };

  const handlePasswordChange = (e) => {
    const value = e.target.value;
    if (/^[a-zA-Z0-9!@#$%]*$/.test(value) && value.length <= 20) {
      setPassword(value);
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={handleUsernameChange}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={handlePasswordChange}
      />
      <button onClick={handleLogin}>Login</button>
    </div>
  );
};

export default Login;


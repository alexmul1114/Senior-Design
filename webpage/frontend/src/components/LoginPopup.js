import React from 'react';
import './LoginPopup.css';

const LoginPopup = ({ onClose }) => {
  return (
    <div className="login-popup">
      <div className="popup-overlay" onClick={onClose}></div>
      <div className="popup-content">
        <h2>Log In</h2>
        <input type="email" placeholder="Email" />
        <input type="password" placeholder="Password" />
        <button>Log In</button>
        <button className="close-btn" onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default LoginPopup;
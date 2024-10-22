import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import LoginPopup from './LoginPopup';
import logo from '../assets/logo.png';
import './NavBar.css';

const NavBar = () => {
  const [showLoginPopup, setShowLoginPopup] = useState(false);
  const navigate = useNavigate();

  const handleLogoClick = () => {
    navigate('/');
  };

  const handleProfileClick = () => {
    // If not logged in, show login popup
    setShowLoginPopup(true);
  };

  return (
    <div className="nav-bar">
      <img src={logo} alt="Logo" className="logo" onClick={handleLogoClick} />
      <input type="text" placeholder="Search..." className="search-bar" />
      <button className="images-button" onClick={() => navigate('/images')}>Images</button>
      <div className="profile-icon" onClick={handleProfileClick}>
        <span>👤</span>
      </div>
      {showLoginPopup && <LoginPopup onClose={() => setShowLoginPopup(false)} />}
    </div>
  );
};

export default NavBar;
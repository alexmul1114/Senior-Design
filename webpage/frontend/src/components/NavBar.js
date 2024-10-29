import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import LoginPopup from './LoginPopup';
import logo from '../assets/logo.png';
import profile from '../assets/profile.png';
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
      <button className="images-button" onClick={() => navigate('/images')}>Upload Images</button>
      <img src={profile} alt="Profile" className="logo" onClick={handleProfileClick} />
      {showLoginPopup && <LoginPopup onClose={() => setShowLoginPopup(false)} />}
    </div>
  );
};

export default NavBar;
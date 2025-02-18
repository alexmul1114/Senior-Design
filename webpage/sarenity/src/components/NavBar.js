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
    setShowLoginPopup(false);
  };

  return (
    <div className="nav-bar">
      <img src={logo} alt="Logo" className="logo" onClick={handleLogoClick} />
      <button className="nav-button" onClick={() => navigate('/')}>Home Page</button>
      <button className="nav-button" onClick={() => navigate('/images')}>Upload Images</button>
      <button className="nav-button" onClick={() => navigate('/results')}>Results</button>
      <button className="nav-button" onClick={() => navigate('/about-us')}>About SARenity</button>
      <button className="nav-button" onClick={() => navigate('/examples')}>Example</button>
      <img src={profile} alt="Profile" className="logo" onClick={handleProfileClick} />
      {showLoginPopup && <LoginPopup onClose={() => setShowLoginPopup(false)} />}
    </div>
  );
};

export default NavBar;
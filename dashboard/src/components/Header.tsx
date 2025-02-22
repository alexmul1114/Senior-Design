import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Header.css';

const Header: React.FC = () => {
  const navigate = useNavigate();

  const handleLogoClick = () => {
    // Redirect to an external website when the logo is clicked
    window.location.href = 'https://www.example.com';
  };

  return (
    <header className="header-container">
      <div className="header-left">
        <div className="logo" onClick={handleLogoClick}>
          LOGO
        </div>
      </div>
      <div className="header-right">
        <button className="nav-button" onClick={() => navigate(-1)}>
          &#8592;
        </button>
        <button className="nav-button" onClick={() => navigate(1)}>
          &#8594;
        </button>
        <div className="profile-button">
          Profile
        </div>
      </div>
    </header>
  );
};

export default Header;

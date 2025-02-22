import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Navigation.css';

const Navigation: React.FC = () => {
  const navigate = useNavigate();

  return (
    <nav className="navigation-container">
      <button onClick={() => navigate('/')} title="Home">
        Home
      </button>
      <button onClick={() => navigate('/documents')} title="Documents">
        Docs
      </button>
      <button onClick={() => navigate('/stats')} title="Stats">
        Stats
      </button>
      <button onClick={() => navigate('/market')} title="Market">
        Market
      </button>
      <button onClick={() => navigate('/advertising')} title="Advertising">
        Ads
      </button>
      <button onClick={() => navigate('/contact')} title="Contact">
        Contact
      </button>
    </nav>
  );
};

export default Navigation;

import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Navigation.css';

const Navigation: React.FC = () => {
  const navigate = useNavigate();

  return (
    <nav className="navigation-container">
      <button className="nav-button" onClick={() => navigate('/')} title="Home">
        <img src="/icons8-home-button-50.png" alt="Home" className="nav-icon" />
      </button>
      <button className="nav-button" onClick={() => navigate('/Documents')} title="Documents">
        <img src="/icons8-document-50.png" alt="Documents" className="nav-icon" />
      </button>
      <button className="nav-button" onClick={() => navigate('/Stats')} title="Stats">
        <img src="/icons8-positive-dynamic-50.png" alt="Stats" className="nav-icon" />
      </button>
      <button className="nav-button" onClick={() => navigate('/Contact')} title="Contact">
        <img src="/icons8-chat-message-50.png" alt="Contact" className="nav-icon" />
      </button>
      <button className="nav-button" onClick={() => navigate('/Market')} title="Marketing">
        <img src="/icons8-market-48.png" alt="Marketing" className="nav-icon" />
      </button>
      <button className="nav-button" onClick={() => navigate('/Advertising')} title="Advertising">
        <img src="/icons8-web-advertising-48.png" alt="Advertising" className="nav-icon" />
      </button>
      <div className="icon-attribution">
        <a target="_blank" rel="noopener noreferrer" href="https://icons8.com">
          Icons8
        </a>
      </div>
    </nav>
  );
};

export default Navigation;

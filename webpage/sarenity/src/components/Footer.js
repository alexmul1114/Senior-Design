import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <button onClick={() => window.location.href = '/about-us'}>About Us</button>
      <span>Contact: contact@sarenity.com</span>
    </footer>
  );
};

export default Footer;
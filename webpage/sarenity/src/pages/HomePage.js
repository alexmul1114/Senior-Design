import React from 'react';
import { useNavigate } from 'react-router-dom';
import SlideShow from '../components/SlideShow';
import Footer from '../components/Footer';
import './HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();
  return (
    <div className="home-page">
      <h1 className="title">SARenity</h1>
      <p className="description">Synthetic Aperture Radar (SAR) imaging explained...</p>
      <SlideShow />
      <button className="get-started-btn" onClick={() => navigate('/images')}>Get Started</button>
      <Footer />
    </div>
  );
};

export default HomePage;
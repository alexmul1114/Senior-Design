import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './components/Header';
import Navigation from './components/Navigation';
import OptionsBar from './components/OptionsBar';
import './App.css';

const App: React.FC = () => {
  return (
    <div className="app-container">
      <Header />
      <div className="main-layout">
        <Navigation />
        <OptionsBar />
        <div className="content-wrapper">
          {/* Nested routes render here */}
          <Outlet />
        </div>
      </div>
    </div>
  );
};

export default App;

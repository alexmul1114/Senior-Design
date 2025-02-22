import React from 'react';
import './ContentArea.css';

const ContentArea: React.FC = () => {
  return (
    <div className="content-area">
      {/* This can be used if you prefer to nest routes here */}
      {/* Or just show something if not using nested routes */}
      <h2>Content Area</h2>
    </div>
  );
};

export default ContentArea;

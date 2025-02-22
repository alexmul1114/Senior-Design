import React from 'react';
import './OptionsBar.css';

const OptionsBar: React.FC = () => {
  return (
    <aside className="options-bar">
      {/* Unique selection content can go here */}
      <h3>Options</h3>
      <p>Adjust settings for this page...</p>
    </aside>
  );
};

export default OptionsBar;

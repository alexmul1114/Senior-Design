import React from 'react';
import DragDrop from '../components/DragDrop';
import Footer from '../components/Footer';
import './ImagesPage.css';

const ImagesPage = () => {
  return (
    <div className="images-page">
      <div className="left-panel">
        <div className="existing-images">
          <h3>Existing Images</h3>
          <ul></ul>
        </div>
        <div className="your-images">
          <h3>Your Images</h3>
          <DragDrop />
        </div>
      </div>
      <div className="right-panel">
        <select>
          <option value="">Select item to search for...</option>
          <option value="car">Car</option>
          <option value="plane">Plane</option>
        </select>
        <button>Submit</button>
      </div>
      <Footer />
    </div>
  );
};

export default ImagesPage;
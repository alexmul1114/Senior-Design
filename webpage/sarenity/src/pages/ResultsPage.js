import React, { useState } from 'react';
import DragDrop from '../components/DragDrop';
import Footer from '../components/Footer';
import ImageGallery from '../components/ImageGallery';
import SelectedImagesTable from '../components/SelectedImagesTable';
import './ImagesPage.css';

const ImagesPage = () => {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleImageUpdate = () => {
    // Update the refresh trigger to force re-render of SelectedImagesTable
    setRefreshTrigger((prev) => prev + 1);
  };
  return (
    <div className="images-page">
      <div className="left-panel">
        <div className="your-images">
          <h1 className="title-images">Images:</h1>
          <ImageGallery onImageUpdate={handleImageUpdate} />
          <DragDrop />
        </div>
      </div>
      <div className="right-panel">
        <h1 className="title-images">Selected Images:</h1>
        <SelectedImagesTable refreshTrigger={refreshTrigger} />
        <button className="submit-btn">Submit</button>
      </div>
      <Footer />
    </div>
  );
};

export default ImagesPage;
import React from 'react';
import DragDrop from '../components/DragDrop';
import Footer from '../components/Footer';
import ImageGallery from '../components/ImageGallery';
import SelectedImagesTable from '../components/SelectedImagesTable';
import './ImagesPage.css';

const ImagesPage = () => {
  return (
    <div className="images-page">
      <div className="left-panel">
        <div className="your-images">
          <h1 className="title-images">Images:</h1>
          <ImageGallery />
          <DragDrop />
        </div>
      </div>
      <div className="right-panel">
        <h1 className="title-images">Selected Images:</h1>
        <SelectedImagesTable />
        <button className="submit-btn">Submit</button>
      </div>
      <Footer />
    </div>
  );
};

export default ImagesPage;
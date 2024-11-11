import React, { useEffect, useState } from 'react';
import './SelectedImagesTable.css';

// Using require.context to dynamically load all images from assets/selectedImages folder
const importAll = (requireContext) => requireContext.keys().map(requireContext);
const images = importAll(require.context('../assets/selectedImages', false, /\.(png|jpe?g|svg)$/)).map((src) => ({
  src,
  name: src.split('/').pop(),
  size: Math.floor(Math.random() * 100) + 50 // Mock size in KB for demonstration purposes
}));

const SelectedImagesTable = () => {
  const [selectedImages, setSelectedImages] = useState(images);

  const handleCategoryChange = (index, newCategory) => {
    const updatedImages = [...selectedImages];
    updatedImages[index].category = newCategory;
    setSelectedImages(updatedImages);
  };

  const handleRemoveImage = (index) => {
    const updatedImages = selectedImages.filter((_, i) => i !== index);
    setSelectedImages(updatedImages);
    // Simulate removing the file from the assets/selectedImages folder
    console.log(`Removed image: ${selectedImages[index].name}`);
  };

  const totalSize = selectedImages.reduce((total, image) => total + image.size, 0);

  return (
    <div className="selected-images-table-container">
      <table className="selected-images-table">
        <thead>
          <tr>
            <th>File Name</th>
            <th>Size</th>
            <th>Category</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {selectedImages.map((image, index) => (
            <tr key={index}>
              <td>{image.name}</td>
              <td>{image.size} KB</td>
              <td>
                <select
                  value={image.category || ''}
                  onChange={(e) => handleCategoryChange(index, e.target.value)}
                >
                  <option value="">Select Category</option>
                  <option value="boat">Boat</option>
                  <option value="plane">Plane</option>
                </select>
              </td>
              <td>
                <button className="remove-button" onClick={() => handleRemoveImage(index)}>x</button>
              </td>
            </tr>
          ))}
          <tr className="totals-row">
            <td><strong>Total</strong></td>
            <td><strong>{totalSize} KB</strong></td>
            <td></td>
            <td></td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default SelectedImagesTable; 
import React, { useEffect, useState } from 'react';
import './SelectedImagesTable.css';

const SelectedImagesTable = ({ refreshTrigger }) => {
  const [selectedImages, setSelectedImages] = useState([]);

  const fetchSelectedImages = async () => {
    try {
      const response = await fetch('https://rocky-crag-89815-04ddc2eb6beb.herokuapp.com/selected-images');
      const data = await response.json();
      const imagesData = await Promise.all(data.map(async (img) => {
        const response = await fetch(img.url);
        const blob = await response.blob();
        const size = blob.size / 1024; // Convert size to KB
        return {
          src: img.url,
          name: img.name,
          size: Math.round(size * 100) / 100, // Round to 2 decimal places
        };
      }));
      setSelectedImages(imagesData);
    } catch (error) {
      console.error('Error fetching selected images:', error);
    }
  };

  useEffect(() => {
    // Initial fetch
    fetchSelectedImages();

    // Set up polling to fetch images every 5 seconds
    const intervalId = setInterval(fetchSelectedImages, 500);

    // Clean up interval on component unmount
    return () => clearInterval(intervalId);
  }, [refreshTrigger]);

  const handleCategoryChange = (index, newCategory) => {
    const updatedImages = [...selectedImages];
    updatedImages[index].category = newCategory;
    setSelectedImages(updatedImages);
  };

  const handleRemoveImage = async (index) => {
    const imageName = selectedImages[index].name;
    try {
      // Call the backend to remove the image from the selectedImages folder
      await fetch('https://rocky-crag-89815-04ddc2eb6beb.herokuapp.com/remove-image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ imageName }),
      });
      // Remove image from local state
      const updatedImages = selectedImages.filter((_, i) => i !== index);
      setSelectedImages(updatedImages);
    } catch (error) {
      console.error('Error removing image:', error);
    }
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
            <td><strong>{totalSize.toFixed(2)} KB</strong></td>
            <td></td>
            <td></td>
          </tr>
        </tbody>
      </table>
    </div>
  );
};

export default SelectedImagesTable;

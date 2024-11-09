import React, { useState, useEffect } from 'react';
import './ImageGallery.css';

// Using require.context to dynamically load all images from assets/images folder
const importAll = (requireContext) => requireContext.keys().map(requireContext);
const images = importAll(require.context('../assets/images', false, /\.(png|jpe?g|svg)$/)).map((src, index) => ({
  src,
  name: src.split('/').pop()
}));

const ImageGallery = () => {
  const [selectedImages, setSelectedImages] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [columnCount, setColumnCount] = useState(3);
  const [filteredImages, setFilteredImages] = useState(images);

  useEffect(() => {
    setFilteredImages(
      images.filter((image) =>
        image.name.toLowerCase().includes(searchTerm.toLowerCase())
      )
    );
  }, [searchTerm]);

  const toggleSelectImage = (index) => {
    setSelectedImages((prevSelectedImages) => {
      if (prevSelectedImages.includes(index)) {
        return prevSelectedImages.filter((i) => i !== index);
      } else {
        return [...prevSelectedImages, index];
      }
    });
  };

  const handleAddColumn = () => {
    setColumnCount((prevCount) => (prevCount < 5 ? prevCount + 1 : 3));
  };

  const calculateGalleryHeight = () => {
    const rowCount = Math.ceil(filteredImages.length / columnCount);
    const rowHeight = 200; // Approximate height for each row, including padding
    return Math.min(rowCount * rowHeight, 700);
  };

  return (
    <div className="image-gallery-container">
      <div className="search-bar-container">
        <input
          type="text"
          placeholder="Search images..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-bar"
        />
        <button onClick={handleAddColumn} className="add-column-button">+</button>
      </div>
      <div
        className="image-gallery"
        style={{ gridTemplateColumns: `repeat(${columnCount}, 1fr)`, height: `${calculateGalleryHeight()}px` }}
      >
        {filteredImages.map((image, index) => (
          <div
            key={index}
            className={`image-item ${selectedImages.includes(index) ? 'selected' : ''}`}
            onClick={() => toggleSelectImage(index)}
          >
            <img src={image.src} alt={`Preview ${index + 1}`} />
            <p className="image-filename">{image.name.substring(0, 12)}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ImageGallery;
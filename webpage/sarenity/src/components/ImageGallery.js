import React, { useState, useEffect } from 'react';
import './ImageGallery.css';

const ImageGallery = ({ onImageUpdate }) => {
  const [selectedImages, setSelectedImages] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [columnCount, setColumnCount] = useState(3);
  const [images, setImages] = useState([]);
  const [filteredImages, setFilteredImages] = useState([]);

  useEffect(() => {
    // Fetch images from the backend hosted on Heroku
    const fetchImages = async () => {
      try {
        const response = await fetch('https://rocky-crag-89815-04ddc2eb6beb.herokuapp.com/images');
        const data = await response.json();
        const imagesData = data.map((img) => ({
          src: img.url,
          name: img.name,
        }));
        setImages(imagesData);
        setFilteredImages(imagesData);
      } catch (error) {
        console.error('Error fetching images:', error);
      }
    };
    fetchImages();
  }, []);

  useEffect(() => {
    setFilteredImages(
      images.filter((image) =>
        image.name.toLowerCase().includes(searchTerm.toLowerCase())
      )
    );
  }, [searchTerm, images]);

  const toggleSelectImage = async (index) => {
    const image = images[index];
    setSelectedImages((prevSelectedImages) => {
      if (prevSelectedImages.includes(index)) {
        // Remove image from selection
        removeImageFromSelected(image.name);
        return prevSelectedImages.filter((i) => i !== index);
      } else {
        // Add image to selection
        addImageToSelected(image.name);
        return [...prevSelectedImages, index];
      }
    });
  };

  const addImageToSelected = async (imageName) => {
    try {
      await fetch('https://rocky-crag-89815-04ddc2eb6beb.herokuapp.com/add-image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ imageName }),
      });
      if (onImageUpdate) {
        onImageUpdate();
      }
    } catch (error) {
      console.error('Error adding image to selected folder:', error);
    }
  };

  const removeImageFromSelected = async (imageName) => {
    try {
      await fetch('https://rocky-crag-89815-04ddc2eb6beb.herokuapp.com/remove-image', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ imageName }),
      });
      if (onImageUpdate) {
        onImageUpdate();
      }
    } catch (error) {
      console.error('Error removing image from selected folder:', error);
    }
  };

  const handleAddColumn = () => {
    setColumnCount((prevCount) => (prevCount < 5 ? prevCount + 1 : 3));
  };

  const calculateGalleryHeight = () => {
    //const rowCount = Math.ceil(filteredImages.length / columnCount);
    //const rowHeight = 200; // Approximate height for each row, including padding
    return window.innerHeight * 0.4;
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

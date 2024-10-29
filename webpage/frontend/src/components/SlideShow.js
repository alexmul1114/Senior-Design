import React, { useState } from 'react';
import './SlideShow.css';
import slideImage1 from '../assets/slide1.png';
import slideImage2 from '../assets/slide2.png';
import slideImage3 from '../assets/slide3.png';

const SlideShow = () => {
  const slides = [
    <img src={slideImage1} alt="Slide 1" />,
    <img src={slideImage2} alt="Slide 2" />,
    <img src={slideImage3} alt="Slide 3" />
  ];
  const [currentSlide, setCurrentSlide] = useState(0);

  const setSlide = (index) => {
    setCurrentSlide(index);
  };

  return (
    <div className="slideshow">
      <div className="slide">{slides[currentSlide]}</div>
      <div className="slide-buttons">
        {slides.map((_, index) => (
          <button
            key={index}
            className={`slide-button ${currentSlide === index ? 'active' : ''}`}
            onClick={() => setSlide(index)}
          ></button>
        ))}
      </div>
    </div>
  );
};

export default SlideShow;

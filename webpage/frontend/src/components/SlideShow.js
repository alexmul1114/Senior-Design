import React, { useState } from 'react';
import './SlideShow.css';

const SlideShow = () => {
  const slides = [
    'Slide 1', 'Slide 2', 'Slide 3' // Replace with slide descriptions or images
  ];
  const [currentSlide, setCurrentSlide] = useState(0);

  const nextSlide = () => {
    setCurrentSlide((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentSlide((prev) => (prev - 1 + slides.length) % slides.length);
  };

  return (
    <div className="slideshow">
      <button onClick={prevSlide}>❮</button>
      <div className="slide">{slides[currentSlide]}</div>
      <button onClick={nextSlide}>❯</button>
    </div>
  );
};

export default SlideShow;
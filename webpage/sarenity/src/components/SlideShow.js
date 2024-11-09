import React, { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SlideShow.css';

// Using require.context to dynamically load all images from assets/homePageSlides folder
const importAll = (requireContext) => requireContext.keys().map(requireContext);
const slides = importAll(require.context('../assets/homePageSlides', false, /\.(png|jpe?g|svg)$/)).map((src, index) => (
  <img src={src} alt={`Slide ${index + 1}`} key={index} />
));

const SlideShow = () => {
  const slideshowRef = useRef(null);
  const [duplicationCount, setDuplicationCount] = useState(0);
  const navigate = useNavigate();

  const handleScroll = () => {
    const slideshow = slideshowRef.current;
    if (slideshow.scrollLeft + slideshow.clientWidth >= slideshow.scrollWidth && duplicationCount < 2) {
      // Duplicate slides to create an infinite loop effect, limit to 2 duplications
      slideshow.innerHTML += slideshow.innerHTML;
      setDuplicationCount(duplicationCount + 1);
    } else if (slideshow.scrollLeft + slideshow.clientWidth >= slideshow.scrollWidth && duplicationCount === 2) {
      // Navigate to the upload images page when reaching the end
      navigate('./images');
    }
  };

  const handleClick = () => {
    const slideshow = slideshowRef.current;
    const slideWidth = 800; // Scroll by one slide width
    slideshow.scrollBy({ left: slideWidth, behavior: 'smooth' });
  };

  return (
    <div className="slideshow-container" ref={slideshowRef} onScroll={handleScroll} onClick={handleClick}>
      <div className="slides">
        {slides}
      </div>
    </div>
  );
};

export default SlideShow;
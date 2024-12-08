import React, { useRef, useState, useEffect } from 'react';
import './SlideShow.css';

// Using require.context to dynamically load all images and videos from assets/homePageSlides folder
const importAll = (requireContext) => requireContext.keys().map(requireContext);
const slides = importAll(require.context('../assets/homePageSlides', false, /\.(png|jpe?g|svg|mp4|webm)$/)).map((src, index) => {
    return <video src={src} key={index} className="slide-video" />;
});

const SlideShow = () => {
  const slideshowRef = useRef(null);
  const [isHovered, setIsHovered] = useState(false);
  const [shiftCount, setShiftCount] = useState(0);
  const [initialScrollLeft, setInitialScrollLeft] = useState(0);
  const [currentVideoIndex, setCurrentVideoIndex] = useState(0);

  useEffect(() => {
    const videoElements = document.querySelectorAll('.slide-video');
    videoElements.forEach(video => {
      video.style.border = 'none';
    });
    
    if (videoElements.length > 0 && currentVideoIndex < videoElements.length) {
      const currentVideo = videoElements[currentVideoIndex];
      currentVideo.play();
      currentVideo.onended = () => {
        // After the video ends, shift to the next slide
        const slideshow = slideshowRef.current;
        if (slideshow) {
          const shiftDistance = currentVideoIndex === 0 ? 600 : 800;
          slideshow.scrollBy({ left: shiftDistance, behavior: 'smooth', duration: 2000 });
        }
        setCurrentVideoIndex((prevIndex) => prevIndex + 1);
      };
    }
  }, [currentVideoIndex]);

  const handleScroll = () => {
    const slideshow = slideshowRef.current;
    if (slideshow.scrollLeft + slideshow.clientWidth >= slideshow.scrollWidth) {
      // Reset to the start when reaching the end
      slideshow.scrollTo({ left: 0, behavior: 'smooth' });
      setShiftCount(0); // Reset shift count for first shift
    }
  };

  const handleMouseEnter = () => {
    setIsHovered(true);
    const slideshow = slideshowRef.current;
    if (slideshow) {
      setInitialScrollLeft(slideshow.scrollLeft); // Store the initial scroll position
    }
  };

  const handleMouseLeave = () => {
    setIsHovered(false);
    const slideshow = slideshowRef.current;
    if (slideshow) {
      slideshow.scrollTo({ left: initialScrollLeft, behavior: 'smooth' }); // Scroll back to the initial position
    }
  };

  const handleClick = () => {
    const slideshow = slideshowRef.current;
    const slideWidth = slideshow.clientWidth; // Get the current slide width dynamically
    const newScrollLeft = slideshow.scrollLeft + slideWidth;
    slideshow.scrollTo({ left: newScrollLeft, behavior: 'smooth' });
  };

  return (
    <div
      className="slideshow-container"
      ref={slideshowRef}
      onScroll={handleScroll}
      onClick={handleClick}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
    >
      <div className="slides">
        {slides}
      </div>
    </div>
  );
};

export default SlideShow;

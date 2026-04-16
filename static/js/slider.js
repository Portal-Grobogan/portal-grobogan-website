/**
 * Alpine.js Hero Slider component data function.
 * Usage: x-data="heroSlider(slides)"
 */
window.heroSlider = function (slides = []) {
  return {
    slides,
    current: 0,
    autoplayInterval: null,

    init() {
      if (this.slides.length > 1) {
        this.startAutoplay();
      }
    },

    startAutoplay() {
      this.stopAutoplay();
      this.autoplayInterval = setInterval(() => {
        this.next();
      }, 5000);
    },

    stopAutoplay() {
      if (this.autoplayInterval) {
        clearInterval(this.autoplayInterval);
        this.autoplayInterval = null;
      }
    },

    next() {
      this.current = (this.current + 1) % this.slides.length;
    },

    prev() {
      this.current = (this.current - 1 + this.slides.length) % this.slides.length;
    },

    goTo(index) {
      this.current = index;
      this.stopAutoplay();
      this.startAutoplay();
    },

    isActive(index) {
      return this.current === index;
    },
  };
};

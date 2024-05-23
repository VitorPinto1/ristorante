document.addEventListener('scroll', function() {
  const sections = document.querySelectorAll('.scroll-section');
  sections.forEach(section => {
      const rect = section.getBoundingClientRect();
      if (rect.top >= 0 && rect.bottom <= window.innerHeight) {
          section.style.transform = 'scale(1.1)';
      } else {
          section.style.transform = 'scale(1)';
      }
  });
});


document.addEventListener('DOMContentLoaded', function() {
  const menuImage = document.querySelector('.img-animate');
  let hasEnteredView = false;

  function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  }

  function onScroll() {
    if (isElementInViewport(menuImage) && !hasEnteredView) {
      menuImage.classList.add('visible');
      hasEnteredView = true;
    }
  }

  window.addEventListener('scroll', onScroll);
  onScroll(); 
});


document.addEventListener('DOMContentLoaded', function() {
  const formElement = document.querySelector('.form-animate');
  let hasEnteredView = false;

  function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
      rect.top >= 0 &&
      rect.left >= 0 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
  }

  function onScroll() {
    if (isElementInViewport(formElement) && !hasEnteredView) {
      formElement.classList.add('visible');
      hasEnteredView = true;
    }
  }

  window.addEventListener('scroll', onScroll);
  onScroll(); 
});

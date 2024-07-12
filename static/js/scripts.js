// Add scaling effect to sections when they are in view
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

// Animate menu image when it enters the viewport for the first time
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

// Animate form element when it enters the viewport using IntersectionObserver
document.addEventListener('DOMContentLoaded', function() {
  const formElement = document.querySelector('.form-animate');
  function onIntersection(entries, observer) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        formElement.classList.add('visible');
        observer.unobserve(entry.target); 
      }
    });
  }
  const observer = new IntersectionObserver(onIntersection, {
    threshold: [0, 0.25, 0.5, 0.75, 1] 
  });
  observer.observe(formElement);
});

// Add 'stay' class to logo when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', (event) => {
  const logo = document.getElementById('logo-image');
  logo.classList.add('stay'); 
});

// Show footer when 'about_us-section' enters the viewport and hide when out
window.addEventListener('scroll', function() {
  var aboutUsSection = document.getElementById('about_us-section');
  var footer = document.getElementById('footer');
  var rect = aboutUsSection.getBoundingClientRect();
  var isEnteringView = (rect.top < window.innerHeight) && (rect.bottom > 0);
  var isOutOfView = (rect.bottom < 0) || (rect.top > window.innerHeight);
  if (isEnteringView) {
    footer.classList.add('visible');
  } else if (isOutOfView) {
    footer.classList.remove('visible');
  }
});

// Automatically close the navbar when a nav link is clicked or outside is clicked
document.addEventListener('DOMContentLoaded', function() {
  var navbarCollapse = document.getElementById('navbarSupportedContent');
  var navLinks = document.querySelectorAll('.navbar-nav .nav-link');
  var navbarToggler = document.querySelector('.navbar-toggler');
  function closeNavbar() {
    var bsCollapse = new bootstrap.Collapse(navbarCollapse, {
      toggle: false
    });
    bsCollapse.hide();
  }
  navLinks.forEach(function(link) {
    link.addEventListener('click', closeNavbar);
  });
  navbarToggler.addEventListener('click', closeNavbar);
  document.addEventListener('click', function(event) {
    var isClickInside = navbarCollapse.contains(event.target) || navbarToggler.contains(event.target);
    if (!isClickInside && navbarCollapse.classList.contains('show')) {
      closeNavbar();
    }
  });
});
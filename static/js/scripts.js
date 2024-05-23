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
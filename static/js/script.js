// Mobile menu toggle
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');

if (hamburger) {
  hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('open');
    navLinks.style.display = navLinks.classList.contains('open') ? 'flex' : 'none';
    if (navLinks.classList.contains('open')) {
      navLinks.style.flexDirection = 'column';
      navLinks.style.position = 'absolute';
      navLinks.style.top = '64px';
      navLinks.style.left = '0';
      navLinks.style.right = '0';
      navLinks.style.background = '#fffaf6';
      navLinks.style.padding = '20px 24px';
      navLinks.style.borderBottom = '1px solid #f0e0d4';
    }
  });
}

// Close mobile menu after clicking a link
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', () => {
    if (navLinks && navLinks.classList.contains('open')) {
      navLinks.classList.remove('open');
      navLinks.style.display = 'none';
    }
  });
});

// Preselect service in the order form when "Order This" is clicked
function preselectService(serviceName) {
  const select = document.getElementById('service');
  if (select) {
    select.value = serviceName;
  }
}

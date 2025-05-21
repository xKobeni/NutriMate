// Intersection Observer for scroll animations
const observerOptions = {
    root: null,
    rootMargin: '-50px',
    threshold: 0.1
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Animate elements when they come into view
document.addEventListener('DOMContentLoaded', () => {
    // Initialize animations
    initializeAnimations();
    
    // Initialize mobile menu
    initializeMobileMenu();
    
    // Initialize smooth scroll
    initializeSmoothScroll();
    
    // Initialize parallax
    initializeParallax();
});

function initializeAnimations() {
    // Animate features with staggered delay
    document.querySelectorAll('.feature-card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.animationDelay = `${index * 0.2}s`;
        observer.observe(card);
    });

    // Animate steps with staggered delay
    document.querySelectorAll('.step-card').forEach((step, index) => {
        step.style.opacity = '0';
        step.style.animationDelay = `${index * 0.3}s`;
        observer.observe(step);
    });

    // Animate other sections
    document.querySelectorAll('.animate-on-scroll').forEach((element) => {
        observer.observe(element);
    });
}

function initializeMobileMenu() {
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
            // Prevent body scroll when menu is open
            document.body.style.overflow = mobileMenu.classList.contains('hidden') ? '' : 'hidden';
        });

        // Close menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!mobileMenu.contains(e.target) && !mobileMenuButton.contains(e.target)) {
                mobileMenu.classList.add('hidden');
                document.body.style.overflow = '';
            }
        });

        // Close menu when clicking a link
        mobileMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
                document.body.style.overflow = '';
            });
        });
    }
}

function initializeSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerOffset = 80; // Adjust based on your header height
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

function initializeParallax() {
    let ticking = false;
    const hero = document.querySelector('.hero-pattern');
    
    if (hero) {
        window.addEventListener('scroll', () => {
            if (!ticking) {
                window.requestAnimationFrame(() => {
                    const scrolled = window.pageYOffset;
                    hero.style.backgroundPositionY = `${scrolled * 0.5}px`;
                    ticking = false;
                });
                ticking = true;
            }
        });
    }
}

// Active navbar link on scroll
const navLinks = document.querySelectorAll('.bg-gray-100 a');
const sections = [
    { id: 'home', link: '#home' },
    { id: 'features', link: '#features' },
    { id: 'how-it-works', link: '#how-it-works' },
    { id: 'contact', link: '#contact' }
];

function setActiveNavLink() {
    let scrollPos = window.scrollY + 120; // Offset for fixed navbar
    let found = false;
    for (let i = sections.length - 1; i >= 0; i--) {
        const section = document.getElementById(sections[i].id);
        if (section && scrollPos >= section.offsetTop) {
            navLinks.forEach(link => {
                link.classList.remove('bg-gradient-to-tr', 'from-green-400', 'to-teal-400', 'text-white', 'shadow');
                link.classList.add('text-gray-700');
            });
            const activeLink = document.querySelector(`.bg-gray-100 a[href='${sections[i].link}']`);
            if (activeLink) {
                activeLink.classList.add('bg-gradient-to-tr', 'from-green-400', 'to-teal-400', 'text-white', 'shadow');
                activeLink.classList.remove('text-gray-700');
            }
            found = true;
            break;
        }
    }
    // If at the very top, ensure Home is active
    if (!found) {
        navLinks.forEach(link => {
            link.classList.remove('bg-gradient-to-tr', 'from-green-400', 'to-teal-400', 'text-white', 'shadow');
            link.classList.add('text-gray-700');
        });
        const homeLink = document.querySelector(`.bg-gray-100 a[href='#home']`);
        if (homeLink) {
            homeLink.classList.add('bg-gradient-to-tr', 'from-green-400', 'to-teal-400', 'text-white', 'shadow');
            homeLink.classList.remove('text-gray-700');
        }
    }
}

window.addEventListener('scroll', setActiveNavLink);
document.addEventListener('DOMContentLoaded', setActiveNavLink);

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});

// Form validation
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}); 
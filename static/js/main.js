/* Main JavaScript for Portfolio Site */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Smooth scrolling for anchor links
    initializeSmoothScroll();
    
    // Mobile menu toggle
    initializeMobileMenu();
});

/* ===================== TOOLTIPS ===================== */
function initializeTooltips() {
    // Initialize Bootstrap tooltips if available
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/* ===================== SMOOTH SCROLL ===================== */
function initializeSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                const target = document.querySelector(href);
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/* ===================== MOBILE MENU ===================== */
function initializeMobileMenu() {
    const navbarToggle = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggle) {
        navbarToggle.addEventListener('click', () => {
            navbarCollapse.classList.toggle('show');
        });
    }
    
    // Close menu when link is clicked
    document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
        link.addEventListener('click', () => {
            navbarCollapse.classList.remove('show');
        });
    });
}

/* ===================== LAZY LOADING IMAGES ===================== */
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    observer.unobserve(img);
                }
            });
        });
        
        images.forEach(img => imageObserver.observe(img));
    }
}

/* ===================== FORM VALIDATION ===================== */
function validateForm(formSelector) {
    const form = document.querySelector(formSelector);
    
    if (!form) return false;
    
    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

/* ===================== ALERT DISMISSAL ===================== */
function dismissAlert(alertElement) {
    alertElement.style.animation = 'slideUp 0.3s ease forwards';
    setTimeout(() => {
        alertElement.remove();
    }, 300);
}

/* ===================== COPY TO CLIPBOARD ===================== */
function copyToClipboard(text, feedbackElement) {
    navigator.clipboard.writeText(text).then(() => {
        const originalText = feedbackElement.textContent;
        feedbackElement.textContent = 'Copied!';
        setTimeout(() => {
            feedbackElement.textContent = originalText;
        }, 2000);
    });
}

/* ===================== DEBOUNCE UTILITY ===================== */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/* ===================== LOADING STATE ===================== */
function setLoadingState(buttonSelector, isLoading) {
    const button = document.querySelector(buttonSelector);
    
    if (isLoading) {
        button.disabled = true;
        button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
    } else {
        button.disabled = false;
        button.innerHTML = button.dataset.originalText || 'Submit';
    }
}

/* ===================== DARK MODE TOGGLE (Optional) ===================== */
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Initialize dark mode on page load if previously enabled
function initializeDarkMode() {
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }
}

// Call on page load
initializeDarkMode();

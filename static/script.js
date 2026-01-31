// Utility function to show notifications
function showNotification(message, type = 'success') {
    const div = document.createElement('div');
    div.className = 'notification';
    
    if (type === 'success') {
        div.style.background = 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)';
    } else if (type === 'error') {
        div.style.background = 'linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%)';
    } else if (type === 'warning') {
        div.style.background = 'linear-gradient(135deg, #f5af19 0%, #f12711 100%)';
    }
    
    div.textContent = message;
    document.body.appendChild(div);
    
    setTimeout(() => {
        div.style.animation = 'slideInUp 0.3s ease reverse';
        setTimeout(() => div.remove(), 300);
    }, 3000);
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

// Initialize tooltips
function initializeTooltips() {
    const tooltips = document.querySelectorAll('[title]');
    tooltips.forEach(element => {
        element.addEventListener('mouseover', function() {
            // Tooltip already in title attribute
        });
    });
}

// Page load initialization
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.3s';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
});

// Smooth scroll to top button
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Add scroll-to-top button if needed
window.addEventListener('scroll', function() {
    const scrollBtn = document.getElementById('scrollToTopBtn');
    if (scrollBtn) {
        if (window.scrollY > 300) {
            scrollBtn.style.display = 'block';
        } else {
            scrollBtn.style.display = 'none';
        }
    }
});

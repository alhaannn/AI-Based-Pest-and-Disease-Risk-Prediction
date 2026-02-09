// Main JavaScript file for Pest & Disease Risk Prediction System

// ===== Alert Count Update =====
function updateAlertCount() {
  fetch('/alerts/api/unread-count/')
    .then(response => response.json())
    .then(data => {
      const badge = document.getElementById('alert-count');
      if (badge) {
        badge.textContent = data.count || 0;
        if (data.count > 0) {
          badge.style.display = 'inline-flex';
        } else {
          badge.style.display = 'none';
        }
      }
    })
    .catch(error => console.error('Error fetching alert count:', error));
}

// ===== Auto-dismiss alerts =====
document.addEventListener('DOMContentLoaded', function () {
  // Update alert count on page load
  updateAlertCount();

  // Auto-dismiss success messages after 5 seconds
  const alerts = document.querySelectorAll('.alert-success');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.animation = 'slideUp 0.3s ease';
      setTimeout(() => alert.remove(), 300);
    }, 5000);
  });
});

// ===== Chart.js default configuration =====
if (typeof Chart !== 'undefined') {
  Chart.defaults.color = '#cbd5e1';
  Chart.defaults.borderColor = '#334155';
  Chart.defaults.font.family = "'Inter', sans-serif";
}

// ===== Utility Functions =====

// Format date to readable format
function formatDate(dateString) {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateString).toLocaleDateString('en-US', options);
}

// Animate numbers counting up
function animateValue(element, start, end, duration) {
  let startTimestamp = null;
  const step = (timestamp) => {
    if (!startTimestamp) startTimestamp = timestamp;
    const progress = Math.min((timestamp - startTimestamp) / duration, 1);
    element.textContent = Math.floor(progress * (end - start) + start);
    if (progress < 1) {
      window.requestAnimationFrame(step);
    }
  };
  window.requestAnimationFrame(step);
}

// Apply counting animation to stat values on page load
document.addEventListener('DOMContentLoaded', function () {
  const statValues = document.querySelectorAll('.stat-value');
  statValues.forEach(stat => {
    const finalValue = parseInt(stat.textContent);
    if (!isNaN(finalValue)) {
      stat.textContent = '0';
      setTimeout(() => animateValue(stat, 0, finalValue, 1000), 100);
    }
  });
});

// ===== Form Validation Helpers =====
function validateForm(formId) {
  const form = document.getElementById(formId);
  if (!form) return false;

  const requiredFields = form.querySelectorAll('[required]');
  let isValid = true;

  requiredFields.forEach(field => {
    if (!field.value.trim()) {
      field.style.borderColor = '#ef4444';
      isValid = false;
    } else {
      field.style.borderColor = '#334155';
    }
  });

  return isValid;
}

// ===== Confirmation Dialog =====
function confirmDelete(message) {
  return confirm(message || 'Are you sure you want to delete this item?');
}

// ===== Console log for debugging =====
console.log('Pest & Disease Risk Prediction System initialized');

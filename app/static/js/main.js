/* Main JavaScript utilities */

// Show/hide elements
function show(element) {
    if (typeof element === 'string') {
        element = document.getElementById(element);
    }
    if (element) element.classList.remove('hidden');
}

function hide(element) {
    if (typeof element === 'string') {
        element = document.getElementById(element);
    }
    if (element) element.classList.add('hidden');
}

// Toast notifications (basic)
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} fixed top-4 right-4 max-w-sm z-50`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-IN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Format time
function formatTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleTimeString('en-IN', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// API helper
function apiCall(url, options = {}) {
    return fetch(url, {
        headers: {
            'Content-Type': 'application/json',
            ...options.headers
        },
        ...options
    }).then(async res => {
        const data = await res.json();
        if (!res.ok) {
            throw new Error(data.error || data.message || 'API error');
        }
        return data;
    });
}

// Load data with loading state
function loadData(url, elementId) {
    const element = document.getElementById(elementId);
    if (!element) return;

    element.innerHTML = '<div class="text-center py-4">Loading...</div>';

    fetch(url)
        .then(r => r.json())
        .then(data => {
            // Populate element with data
            console.log('Data loaded:', data);
        })
        .catch(err => {
            element.innerHTML = `<div class="text-center py-4 text-red-600">Error loading data</div>`;
            console.error('Load error:', err);
        });
}

// Form serialization
function serializeForm(form) {
    const formData = new FormData(form);
    const data = {};
    for (let [key, value] of formData.entries()) {
        data[key] = value;
    }
    return data;
}

// Confirm dialog
function confirmAction(message) {
    return confirm(message);
}

// URL parameters
function getUrlParam(name) {
    const params = new URLSearchParams(window.location.search);
    return params.get(name);
}

// Initialize
document.addEventListener('DOMContentLoaded', function () {
    // Any global initialization here
});

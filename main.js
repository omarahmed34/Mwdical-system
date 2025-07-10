// AI Medical Assistant - Main JavaScript File
// This file handles common functionality across all pages

document.addEventListener('DOMContentLoaded', () => {
    // Login Modal Functionality
    const loginBtn = document.getElementById('loginBtn');
    const loginModal = document.getElementById('loginModal');
    const closeModal = document.getElementById('closeModal');
    const modalTabs = document.querySelectorAll('.modal-tab');
    const authForms = document.querySelectorAll('.auth-form');

    // Open modal when login button is clicked
    if (loginBtn) {
        loginBtn.addEventListener('click', (e) => {
            e.preventDefault();
            loginModal.classList.add('active');
        });
    }

    // Close modal when close button is clicked
    if (closeModal) {
        closeModal.addEventListener('click', () => {
            loginModal.classList.remove('active');
        });
    }

    // Close modal when clicking outside of it
    if (loginModal) {
        window.addEventListener('click', (e) => {
            if (e.target === loginModal) {
                loginModal.classList.remove('active');
            }
        });
    }

    // Tab switching in modal
    modalTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabType = tab.getAttribute('data-tab');
            
            // Update active tab
            modalTabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            // Show corresponding form
            authForms.forEach(form => form.classList.remove('active'));
            document.getElementById(`${tabType}Form`).classList.add('active');
        });
    });

    // Form submission handling
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');

    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // Add login logic here
            console.log('Login submitted');
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            e.preventDefault();
            // Add registration logic here
            console.log('Registration submitted');
        });
    }

    // Diagnosis page loading overlay
    const symptomForm = document.getElementById('symptomForm');
    const loadingOverlay = document.getElementById('loadingOverlay');

    if (symptomForm && loadingOverlay) {
        symptomForm.addEventListener('submit', (e) => {
            // Show loading overlay
            loadingOverlay.classList.remove('hidden');
        });
    }
});

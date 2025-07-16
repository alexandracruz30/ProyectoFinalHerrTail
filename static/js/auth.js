// Mejoras de UX para formularios de autenticación
document.addEventListener('DOMContentLoaded', function() {
    
    // Auto-focus en el primer campo visible del formulario
    const firstInput = document.querySelector('.auth-input');
    if (firstInput) {
        firstInput.focus();
    }
    
    // Validación en tiempo real para campos de formulario
    const inputs = document.querySelectorAll('.auth-input');
    inputs.forEach(input => {
        input.addEventListener('blur', validateField);
        input.addEventListener('input', clearFieldError);
    });
    
    function validateField(e) {
        const field = e.target;
        const value = field.value.trim();
        
        // Email validation
        if (field.type === 'email' && value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                showFieldError(field, 'Por favor ingresa un email válido');
            }
        }
        
        // Username validation
        if (field.name === 'username' && value) {
            const usernameRegex = /^[\w.@+-]+$/;
            if (!usernameRegex.test(value)) {
                showFieldError(field, 'Solo se permiten letras, números y @/./+/-/_');
            } else if (value.length < 3) {
                showFieldError(field, 'El nombre de usuario debe tener al menos 3 caracteres');
            }
        }
        
        // Required field validation
        if (field.hasAttribute('required') && !value) {
            showFieldError(field, 'Este campo es obligatorio');
        }
    }
    
    function showFieldError(field, message) {
        // Remove existing error
        clearFieldError({ target: field });
        
        // Add error styling
        field.classList.add('border-red-500', 'dark:border-red-400');
        field.classList.remove('border-gray-300', 'dark:border-gray-600');
        
        // Create error message
        const errorDiv = document.createElement('p');
        errorDiv.className = 'text-sm text-red-600 dark:text-red-400 mt-1 field-error';
        errorDiv.textContent = message;
        
        // Insert after the field
        field.parentNode.insertBefore(errorDiv, field.nextSibling);
    }
    
    function clearFieldError(e) {
        const field = e.target;
        
        // Remove error styling
        field.classList.remove('border-red-500', 'dark:border-red-400');
        field.classList.add('border-gray-300', 'dark:border-gray-600');
        
        // Remove error message
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
    }
    
    // Toggle password visibility
    const passwordToggles = document.querySelectorAll('[data-toggle-password]');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const targetId = this.getAttribute('data-toggle-password');
            const passwordField = document.getElementById(targetId);
            
            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                this.innerHTML = '<i class="fas fa-eye-slash"></i>';
            } else {
                passwordField.type = 'password';
                this.innerHTML = '<i class="fas fa-eye"></i>';
            }
        });
    });
    
    // Form animation on error
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('invalid', function(e) {
            e.preventDefault();
            
            // Add shake animation to form
            form.classList.add('animate-shake');
            setTimeout(() => {
                form.classList.remove('animate-shake');
            }, 600);
            
            // Focus first invalid field
            const firstInvalid = form.querySelector(':invalid');
            if (firstInvalid) {
                firstInvalid.focus();
                firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        }, true);
    });
    
    // Auto-save form data to localStorage (except passwords)
    const saveFormData = () => {
        const formData = {};
        inputs.forEach(input => {
            if (input.type !== 'password' && input.value) {
                formData[input.name] = input.value;
            }
        });
        localStorage.setItem('formData', JSON.stringify(formData));
    };
    
    const loadFormData = () => {
        try {
            const savedData = JSON.parse(localStorage.getItem('formData') || '{}');
            inputs.forEach(input => {
                if (input.type !== 'password' && savedData[input.name]) {
                    input.value = savedData[input.name];
                }
            });
        } catch (e) {
            console.log('No saved form data found');
        }
    };
    
    // Load saved data on page load
    loadFormData();
    
    // Save data on input change
    inputs.forEach(input => {
        if (input.type !== 'password') {
            input.addEventListener('input', saveFormData);
        }
    });
    
    // Clear saved data on successful form submission
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            setTimeout(() => {
                localStorage.removeItem('formData');
            }, 1000);
        });
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const submitButton = document.querySelector('button[type="submit"]');
            if (submitButton && !submitButton.disabled) {
                submitButton.click();
            }
        }
    });
    
    // Add loading animation to submit buttons
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (!this.classList.contains('btn-loading')) {
                // Add loading state after a short delay to allow form validation
                setTimeout(() => {
                    if (!this.disabled) {
                        this.classList.add('btn-loading');
                    }
                }, 100);
            }
        });
    });
});

// Utility function to show toast notifications
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg text-white max-w-sm transform transition-all duration-300 translate-x-full ${
        type === 'success' ? 'bg-green-500' :
        type === 'error' ? 'bg-red-500' :
        type === 'warning' ? 'bg-yellow-500' : 'bg-blue-500'
    }`;
    
    toast.innerHTML = `
        <div class="flex items-center">
            <div class="flex-shrink-0">
                <i class="fas ${
                    type === 'success' ? 'fa-check-circle' :
                    type === 'error' ? 'fa-exclamation-circle' :
                    type === 'warning' ? 'fa-exclamation-triangle' : 'fa-info-circle'
                }"></i>
            </div>
            <div class="ml-3">
                <p class="text-sm font-medium">${message}</p>
            </div>
            <div class="ml-4 flex-shrink-0">
                <button class="text-white hover:text-gray-200" onclick="this.parentElement.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    // Animate in
    setTimeout(() => {
        toast.classList.remove('translate-x-full');
    }, 100);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.classList.add('translate-x-full');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 300);
    }, 5000);
}
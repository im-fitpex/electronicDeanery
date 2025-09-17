// Главный JavaScript файл для деканата
(function() {
    'use strict';

    // Инициализация при загрузке DOM
    document.addEventListener('DOMContentLoaded', function() {
        initDropdowns();
        initAlerts();
        initNavbarToggle();
        initFormValidation();
    });

    // Функциональность выпадающих меню
    function initDropdowns() {
        const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
        
        dropdownToggles.forEach(function(toggle) {
            toggle.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                const dropdown = this.closest('.dropdown');
                const menu = dropdown.querySelector('.dropdown-menu');
                
                // Закрываем все другие открытые меню
                closeAllDropdowns();
                
                // Переключаем текущее меню
                if (menu) {
                    menu.classList.toggle('show');
                }
            });
        });

        // Закрытие меню при клике вне его
        document.addEventListener('click', function(e) {
            if (!e.target.closest('.dropdown')) {
                closeAllDropdowns();
            }
        });

        // Закрытие меню при нажатии Escape
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeAllDropdowns();
            }
        });
    }

    function closeAllDropdowns() {
        const openMenus = document.querySelectorAll('.dropdown-menu.show');
        openMenus.forEach(function(menu) {
            menu.classList.remove('show');
        });
    }

    // Функциональность алертов
    function initAlerts() {
        const alertCloseButtons = document.querySelectorAll('.btn-close');
        
        alertCloseButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                const alert = this.closest('.alert');
                if (alert) {
                    // Добавляем анимацию исчезновения
                    alert.style.opacity = '0';
                    alert.style.transition = 'opacity 0.3s ease-in-out';
                    
                    setTimeout(function() {
                        alert.remove();
                    }, 300);
                }
            });
        });

        // Автоматическое скрытие алертов через 5 секунд
        const autoHideAlerts = document.querySelectorAll('.alert[data-auto-hide]');
        autoHideAlerts.forEach(function(alert) {
            setTimeout(function() {
                if (alert.parentNode) {
                    alert.style.opacity = '0';
                    alert.style.transition = 'opacity 0.3s ease-in-out';
                    
                    setTimeout(function() {
                        if (alert.parentNode) {
                            alert.remove();
                        }
                    }, 300);
                }
            }, 5000);
        });
    }

    // Функциональность навигационного меню (бургер-меню)
    function initNavbarToggle() {
        const navbarToggler = document.querySelector('.navbar-toggler');
        const navbarCollapse = document.querySelector('.navbar-collapse');
        
        if (navbarToggler && navbarCollapse) {
            navbarToggler.addEventListener('click', function() {
                navbarCollapse.classList.toggle('show');
            });

            // Закрытие меню при клике на ссылку (для мобильных)
            const navLinks = navbarCollapse.querySelectorAll('.nav-link');
            navLinks.forEach(function(link) {
                link.addEventListener('click', function() {
                    if (window.innerWidth < 768) {
                        navbarCollapse.classList.remove('show');
                    }
                });
            });
        }
    }

    // Базовая валидация форм
    function initFormValidation() {
        const forms = document.querySelectorAll('form[data-validate]');
        
        forms.forEach(function(form) {
            form.addEventListener('submit', function(e) {
                let isValid = true;
                const requiredFields = form.querySelectorAll('[required]');
                
                // Очищаем предыдущие ошибки
                clearFormErrors(form);
                
                requiredFields.forEach(function(field) {
                    if (!field.value.trim()) {
                        showFieldError(field, 'Это поле обязательно для заполнения');
                        isValid = false;
                    }
                });

                // Валидация email
                const emailFields = form.querySelectorAll('input[type="email"]');
                emailFields.forEach(function(field) {
                    if (field.value && !isValidEmail(field.value)) {
                        showFieldError(field, 'Введите корректный email адрес');
                        isValid = false;
                    }
                });

                // Валидация телефона
                const phoneFields = form.querySelectorAll('input[type="tel"]');
                phoneFields.forEach(function(field) {
                    if (field.value && !isValidPhone(field.value)) {
                        showFieldError(field, 'Введите корректный номер телефона');
                        isValid = false;
                    }
                });

                if (!isValid) {
                    e.preventDefault();
                    // Скроллим к первой ошибке
                    const firstError = form.querySelector('.form-error');
                    if (firstError) {
                        firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
            });
        });
    }

    function clearFormErrors(form) {
        const errorMessages = form.querySelectorAll('.form-error');
        errorMessages.forEach(function(error) {
            error.remove();
        });

        const errorFields = form.querySelectorAll('.form-control.is-invalid');
        errorFields.forEach(function(field) {
            field.classList.remove('is-invalid');
        });
    }

    function showFieldError(field, message) {
        field.classList.add('is-invalid');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'form-error text-danger mt-1';
        errorDiv.textContent = message;
        
        field.parentNode.appendChild(errorDiv);
    }

    function isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    function isValidPhone(phone) {
        // Простая валидация для российских номеров
        const phoneRegex = /^[\+]?[7|8][\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}$/;
        return phoneRegex.test(phone.replace(/\s/g, ''));
    }

    // Утилитарные функции
    window.DeaneryApp = {
        // Показать уведомление
        showNotification: function(message, type = 'info') {
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
            alertDiv.innerHTML = `
                ${message}
                <button type="button" class="btn-close" aria-label="Close"></button>
            `;

            const container = document.querySelector('.container');
            if (container) {
                container.insertBefore(alertDiv, container.firstChild);
                
                // Инициализируем кнопку закрытия
                const closeBtn = alertDiv.querySelector('.btn-close');
                if (closeBtn) {
                    closeBtn.addEventListener('click', function() {
                        alertDiv.style.opacity = '0';
                        alertDiv.style.transition = 'opacity 0.3s ease-in-out';
                        setTimeout(() => alertDiv.remove(), 300);
                    });
                }

                // Автоскрытие через 5 секунд
                setTimeout(function() {
                    if (alertDiv.parentNode) {
                        alertDiv.style.opacity = '0';
                        alertDiv.style.transition = 'opacity 0.3s ease-in-out';
                        setTimeout(() => {
                            if (alertDiv.parentNode) {
                                alertDiv.remove();
                            }
                        }, 300);
                    }
                }, 5000);
            }
        },

        // Подтверждение действия
        confirmAction: function(message, callback) {
            if (confirm(message)) {
                callback();
            }
        },

        // Загрузка данных через AJAX
        loadData: function(url, options = {}) {
            const defaultOptions = {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                }
            };

            // Добавляем CSRF токен для POST запросов
            if (options.method === 'POST') {
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
                if (csrfToken) {
                    defaultOptions.headers['X-CSRFToken'] = csrfToken.value;
                }
            }

            const finalOptions = Object.assign(defaultOptions, options);

            return fetch(url, finalOptions)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .catch(error => {
                    console.error('Ошибка загрузки данных:', error);
                    this.showNotification('Произошла ошибка при загрузке данных', 'danger');
                    throw error;
                });
        }
    };

    // Добавляем стили для валидации форм
    const validationStyles = `
        .form-control.is-invalid {
            border-color: #dc3545;
            box-shadow: 0 0 0 0.2rem rgba(220, 53, 69, 0.25);
        }
        
        .form-error {
            font-size: 0.875rem;
            margin-top: 0.25rem;
        }
        
        .fade {
            opacity: 1;
            transition: opacity 0.15s linear;
        }
        
        .fade:not(.show) {
            opacity: 0;
        }
    `;

    // Добавляем стили в head
    const styleSheet = document.createElement('style');
    styleSheet.textContent = validationStyles;
    document.head.appendChild(styleSheet);

})();
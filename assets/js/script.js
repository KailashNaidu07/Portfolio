document.addEventListener('DOMContentLoaded', () => {
    // Initialize Feather Icons
    feather.replace();

    // Mobile Menu Functionality
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');
    const closeIcon = document.getElementById('close-icon');
    let isMenuOpen = false;

    const toggleMenu = () => {
        isMenuOpen = !isMenuOpen;
        mobileMenu.classList.toggle('opacity-100', isMenuOpen);
        mobileMenu.classList.toggle('translate-y-0', isMenuOpen);
        mobileMenu.classList.toggle('pointer-events-auto', isMenuOpen);
        mobileMenu.classList.toggle('opacity-0', !isMenuOpen);
        mobileMenu.classList.toggle('-translate-y-2', !isMenuOpen);
        mobileMenu.classList.toggle('pointer-events-none', !isMenuOpen);
        menuIcon.classList.toggle('hidden', isMenuOpen);
        closeIcon.classList.toggle('hidden', !isMenuOpen);
        document.body.style.overflow = isMenuOpen ? 'hidden' : '';
    };

    mobileMenuButton.addEventListener('click', toggleMenu);

    // Close menu when clicking menu items or resizing
    document.querySelectorAll('#mobile-menu a').forEach(item => {
        item.addEventListener('click', toggleMenu);
    });

    window.addEventListener('resize', () => {
        if (window.innerWidth >= 768 && isMenuOpen) {
            toggleMenu();
        }
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href'))?.scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    // Project filtering
    const filterButtons = document.querySelectorAll('[data-filter]');
    const projectCards = document.querySelectorAll('[data-category]');

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            const filter = button.dataset.filter;
            
            // Update button states
            filterButtons.forEach(btn => {
                btn.classList.toggle('bg-blue-600', btn === button);
                btn.classList.toggle('text-white', btn === button);
                btn.classList.toggle('bg-white', btn !== button);
                btn.classList.toggle('text-gray-700', btn !== button);
            });

            // Filter projects
            projectCards.forEach(card => {
                const shouldShow = filter === 'all' || card.dataset.category === filter;
                card.style.display = shouldShow ? 'block' : 'none';
                card.style.opacity = shouldShow ? '1' : '0';
                card.style.transform = shouldShow ? 'translateY(0)' : 'translateY(20px)';
            });
        });
    });

    // Testimonials slider
    const swiper = new Swiper('.testimonials-slider', {
        effect: 'slide',
        loop: true,
        spaceBetween: 30,
        keyboard: { enabled: true },
        breakpoints: {
            320: { slidesPerView: 1, spaceBetween: 20 },
            768: { slidesPerView: 2, spaceBetween: 30 },
            1024: { slidesPerView: 3, spaceBetween: 30 }
        },
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev',
        },
        pagination: {
            el: '.swiper-pagination',
            clickable: true,
        },
        autoplay: {
            delay: 5000,
            disableOnInteraction: false,
        },
        speed: 800,
        grabCursor: true,
    });

    // Typing animation
    new Typed('.typing-animation', {
        strings: ['Full-Stack Developer', 'Mobile App Developer', 'Front-End Developer'],
        typeSpeed: 50,
        backSpeed: 30,
        backDelay: 1500,
        loop: true
    });

    // Contact form handling
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const button = document.getElementById('submitting-button');
            const originalText = button.innerHTML;
            
            // Show loading state
            button.disabled = true;
            button.innerHTML = `
                <span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                Sending...
            `;
            
            try {
                const formData = new FormData(contactForm);
                const response = await fetch('/api/contact', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                    },
                    body: formData
                });

                const result = await response.json();
                
                if (!response.ok) {
                    throw new Error(result.error || 'Failed to send message');
                }
                
                // Success feedback
                contactForm.reset();
                showAlert('Message sent successfully!', 'success');
                
            } catch (error) {
                showAlert(`Error: ${error.message}`, 'danger');
                console.error('Submission error:', error);
            } finally {
                button.disabled = false;
                button.innerHTML = originalText;
            }
        });
    }

    function showAlert(message, type) {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show mt-4`;
        alertDiv.role = 'alert';
        alertDiv.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;
        
        const container = document.querySelector('.alert-container') || contactForm;
        container.prepend(alertDiv);
        
        setTimeout(() => alertDiv.remove(), 5000);
    }
});
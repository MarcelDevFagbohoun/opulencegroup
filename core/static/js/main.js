
        // Mobile & Sidebar toggles
        function toggleMobileSearch() { document.getElementById('mobile-search').classList.toggle('hidden'); }
        function toggleMobileSidebar() {
            const sidebar = document.getElementById('mobile-sidebar');
            sidebar.classList.toggle('hidden');
            document.body.style.overflow = sidebar.classList.contains('hidden') ? '' : 'hidden';
        }
        function toggleCartSidebar() {
            const sidebar = document.getElementById('cart-sidebar');
            sidebar.classList.toggle('hidden');
            document.body.style.overflow = sidebar.classList.contains('hidden') ? '' : 'hidden';
        }

        // Authentication modal
        function toggleAuthModal() {
            const modal = document.getElementById('auth-modal');
            modal.classList.toggle('hidden');
            document.body.style.overflow = modal.classList.contains('hidden') ? '' : 'hidden';
            if(!modal.classList.contains('hidden')) switchAuthTab('login');
        }
        function switchAuthTab(tab) {
            const loginTab = document.getElementById('login-tab');
            const signupTab = document.getElementById('signup-tab');
            const loginForm = document.getElementById('login-form');
            const signupForm = document.getElementById('signup-form');
            if(tab==='login'){
                loginTab.classList.add('border-primary','text-primary');
                loginTab.classList.remove('border-transparent','text-neutral-600');
                signupTab.classList.remove('border-primary','text-primary');
                signupTab.classList.add('border-transparent','text-neutral-600');
                loginForm.classList.remove('hidden'); signupForm.classList.add('hidden');
            }else{
                signupTab.classList.add('border-primary','text-primary');
                signupTab.classList.remove('border-transparent','text-neutral-600');
                loginTab.classList.remove('border-primary','text-primary');
                loginTab.classList.add('border-transparent','text-neutral-600');
                signupForm.classList.remove('hidden'); loginForm.classList.add('hidden');
            }
        }


// SLIDER
// Hero slideshow functionality
let currentSlide = 0;
const slides = document.querySelectorAll('.hero-slide');
const indicators = document.querySelectorAll('.hero-indicator');
const totalSlides = slides.length;

// Auto-advance slideshow every 20 seconds
let slideInterval = setInterval(nextSlide, 20000);

function showSlide(index) {
    // Remove active class from all slides and indicators
    slides.forEach(slide => {
        slide.classList.remove('active');
        slide.style.opacity = '0';
    });
    indicators.forEach(indicator => indicator.classList.remove('active'));
    
    // Show current slide
    slides[index].classList.add('active');
    slides[index].style.opacity = '1';
    indicators[index].classList.add('active');
    
    currentSlide = index;
}

function nextSlide() {
    const nextIndex = (currentSlide + 1) % totalSlides;
    showSlide(nextIndex);
}

function goToSlide(index) {
    // Clear the auto-advance timer and restart it
    clearInterval(slideInterval);
    showSlide(index);
    slideInterval = setInterval(nextSlide, 20000);
}

// Initialize slideshow
document.addEventListener('DOMContentLoaded', function() {
    // Ensure first slide is visible
    showSlide(0);
});

// Pause slideshow when tab is not visible (performance)
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        clearInterval(slideInterval);
    } else {
        slideInterval = setInterval(nextSlide, 20000);
    }
});


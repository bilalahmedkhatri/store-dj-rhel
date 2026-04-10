/* Global Scripts */
document.addEventListener('DOMContentLoaded', function () {
    // Mobile menu toggle
    const hamburgerBtn = document.getElementById('hamburger');
    const mobileMenu = document.querySelector('.mobile-menu');

    if (hamburgerBtn && mobileMenu) {
        hamburgerBtn.addEventListener('click', function () {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Swiper initialization
    if (typeof Swiper !== 'undefined') {
        new Swiper('.swiper', {
            slidesPerView: 2,
            loop: true,
            autoplay: {
                delay: 3000,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            breakpoints: {
                1024: {
                    slidesPerView: 6,
                },
            },
        });

        new Swiper('.main-slider', {
            slidesPerView: 1,
            loop: true,
            autoplay: {
                delay: 5000,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
        });
    }

    // Search field toggle
    const searchIcon = document.getElementById('search-icon');
    const searchField = document.getElementById('search-field');
    if (searchIcon && searchField) {
        searchIcon.addEventListener('click', function () {
            searchField.classList.toggle('hidden');
            if (!searchField.classList.contains('hidden')) {
                searchField.classList.add('search-slide-down');
            }
        });
    }

    // Storefront view more
    const viewMoreBtn = document.getElementById('storefront-view-more');
    const hiddenCards = Array.from(document.querySelectorAll('.js-more-product.hidden'));
    
    if (viewMoreBtn && hiddenCards.length > 0) {
        let revealedCount = 0;
        const chunkSize = 5;

        viewMoreBtn.addEventListener('click', function () {
            const nextChunk = hiddenCards.slice(revealedCount, revealedCount + chunkSize);
            nextChunk.forEach((card) => card.classList.remove('hidden'));
            revealedCount += nextChunk.length;

            if (revealedCount >= hiddenCards.length) {
                viewMoreBtn.disabled = true;
                viewMoreBtn.classList.add('opacity-60', 'cursor-not-allowed');
                viewMoreBtn.innerHTML = 'No More Items';
            }
        });
    }
    // Products filter toggle (Mobile)
    const filterToggleBtn = document.getElementById('products-toggle-filters');
    const filtersAside = document.getElementById('filters');
    if (filterToggleBtn && filtersAside) {
        filterToggleBtn.addEventListener('click', function () {
            filtersAside.classList.toggle('hidden');
            filterToggleBtn.textContent = filtersAside.classList.contains('hidden') ? 'Show Filters' : 'Hide Filters';
        });
    }
});

// Global utility functions
function toggleDropdown(id, show) {
    const dropdown = document.getElementById(id);
    if (!dropdown) return;
    if (show) {
        dropdown.classList.remove('hidden');
    } else {
        dropdown.classList.add('hidden');
    }
}

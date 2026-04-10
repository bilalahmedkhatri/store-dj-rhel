/**
 * Product Page — Gallery, Quantity, Tabs, AJAX Add-to-Cart
 */
document.addEventListener('DOMContentLoaded', function () {

    // ── 1. Quantity Controls ──────────────────────────────────────
    const qtyInput = document.getElementById('quantity');
    const decreaseBtn = document.getElementById('decrease-qty');
    const increaseBtn = document.getElementById('increase-qty');

    if (qtyInput) {
        if (decreaseBtn) {
            decreaseBtn.addEventListener('click', e => {
                e.preventDefault();
                const val = parseInt(qtyInput.value);
                if (!isNaN(val) && val > 1) qtyInput.value = val - 1;
            });
        }
        if (increaseBtn) {
            increaseBtn.addEventListener('click', e => {
                e.preventDefault();
                e.stopImmediatePropagation();
                const val = parseInt(qtyInput.value);
                if (!isNaN(val)) qtyInput.value = val + 1;
            });
        }

        qtyInput.addEventListener('change', function () {
            const val = parseInt(this.value);
            if (isNaN(val) || val < 1) this.value = 1;
        });
    }

    // ── 2. Gallery Image Switching ────────────────────────────────
    const mainImage = document.getElementById('main-product-image');
    const thumbs = document.querySelectorAll('.thumbnail-btn');

    if (mainImage && thumbs.length > 0) {
        // Set first thumb as active
        if (thumbs[0]) thumbs[0].classList.add('border-primary');

        thumbs.forEach(thumb => {
            const imgUrl = thumb.getAttribute('data-image');
            if (!imgUrl) return;
            thumb.addEventListener('click', e => {
                e.preventDefault();
                // Smooth crossfade
                mainImage.style.opacity = '0';
                setTimeout(() => {
                    mainImage.src = imgUrl;
                    mainImage.style.opacity = '1';
                }, 150);
                thumbs.forEach(t => t.classList.remove('border-primary'));
                thumb.classList.add('border-primary');
            });
        });
        // Crossfade transition style
        mainImage.style.transition = 'opacity 0.15s ease';
    }

    // ── 3. Tab System ─────────────────────────────────────────────
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    if (tabBtns.length > 0) {
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const tabId = btn.getAttribute('data-tab');

                tabBtns.forEach(b => {
                    b.classList.remove('active', 'text-gray-900');
                    b.classList.add('text-gray-500');
                    b.style.borderBottomColor = 'transparent';
                });
                btn.classList.add('active', 'text-gray-900');
                btn.classList.remove('text-gray-500');
                btn.style.borderBottomColor = '';

                tabContents.forEach(c => c.classList.add('hidden'));
                const target = document.getElementById(tabId);
                if (target) target.classList.remove('hidden');
            });
        });
    }

    // ── 4. AJAX Add-to-Cart with Loading / Success States ─────────
    const addToCartForm = document.getElementById('add-to-cart-form');
    const addToCartBtn = document.getElementById('add-to-cart-btn');

    if (addToCartForm && addToCartBtn) {
        addToCartForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            e.stopImmediatePropagation(); // even stronger prevention
            if (addToCartBtn.disabled) return;


            // Store original label
            const originalHTML = addToCartBtn.innerHTML;

            // ── Loading state ──────────────────────────────────────
            addToCartBtn.disabled = true;
            addToCartBtn.innerHTML = `
                <i class="fas fa-circle-notch fa-spin text-lg"></i>
                <span>Adding&hellip;</span>
            `;

            // Wait for cart handler (loaded after this script)
            const engine = window.cartState;
            if (!engine) {
                addToCartBtn.disabled = false;
                addToCartBtn.innerHTML = originalHTML;
                addToCartForm.submit(); // fallback
                return;
            }

            const result = await engine.addToCart(addToCartForm);

            if (result?.success) {
                // ── Success state ──────────────────────────────────
                addToCartBtn.innerHTML = `
                    <i class="fas fa-shopping-bag text-lg"></i>
                    <span>Show Cart</span>
                `;
                addToCartBtn.classList.remove('bg-primary');
                addToCartBtn.classList.add('bg-green-600', 'text-white'); // ✅ FIX
                // Change action to redirect to cart
                addToCartBtn.type = 'button';
                addToCartBtn.onclick = () => window.location.href = '/cart/';

                setTimeout(() => {
                    addToCartBtn.disabled = false;
                }, 500);
                // No automatic revert to "Add to Cart" if success, 
                // we want it to stay as "Show Cart"
            } else {
                // ── Error / fallback ───────────────────────────────
                addToCartBtn.innerHTML = `
                    <i class="fas fa-exclamation-circle text-lg"></i>
                    <span>Try Again</span>
                `;
                setTimeout(() => {
                    addToCartBtn.disabled = false;
                    addToCartBtn.innerHTML = originalHTML;
                }, 2000);
            }
        });
    }


    // ── 5. Check if already in cart ────────────────────────────────
    function checkCartStatus() {
        const productSlug = document.querySelector('input[name="slug"]')?.value;
        if (!productSlug || !window.cartState) return;

        const isInCart = window.cartState.items.some(item => String(item.slug) === String(productSlug));
        if (isInCart && addToCartBtn) {
            addToCartBtn.innerHTML = `
                <i class="fas fa-shopping-bag text-lg"></i>
                <span>Show Cart</span>
            `;
            addToCartBtn.classList.add('bg-secondary');
            addToCartBtn.classList.remove('bg-primary');
            addToCartBtn.type = 'button';
            addToCartBtn.onclick = (e) => {
                e.preventDefault();
                window.location.href = '/cart/';
            };
        }
    }

    // React to cart updates (instant sync)
    document.addEventListener('cart:updated', checkCartStatus);

    // Initial check (slightly delayed to allow hydration)
    setTimeout(checkCartStatus, 300);
});



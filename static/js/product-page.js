/**
 * Product Page — Gallery, Quantity, Tabs, AJAX Add-to-Cart
 */
document.addEventListener('DOMContentLoaded', function () {

    // ── 1. Quantity Controls ──────────────────────────────────────
    const qtyInput = document.getElementById('quantity');
    const decreaseBtn = document.getElementById('decrease-qty');
    const increaseBtn = document.getElementById('increase-qty');

    if (qtyInput && !qtyInput.dataset.eventsAttached) {
        qtyInput.dataset.eventsAttached = "true";
        
        if (decreaseBtn) {
            decreaseBtn.addEventListener('click', e => {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                const val = parseInt(qtyInput.value);
                if (!isNaN(val) && val > 1) qtyInput.value = val - 1;
            });
        }
        if (increaseBtn) {
            increaseBtn.addEventListener('click', e => {
                e.preventDefault();
                e.stopPropagation();
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

    // ── 2. Gallery & Variant Switching ────────────────────────────
    const mainImage = document.getElementById('main-product-image');
    const thumbs = document.querySelectorAll('.thumbnail-btn');
    const variantRadios = document.querySelectorAll('.variant-radio');

    function updateMainImage(url, forceActiveThumb = false) {
        if (!mainImage || !url) return;
        mainImage.style.opacity = '0';
        setTimeout(() => {
            mainImage.src = url;
            mainImage.style.opacity = '1';
        }, 150);

        if (forceActiveThumb) {
            thumbs.forEach(t => {
                if (t.getAttribute('data-image') === url) {
                    t.classList.add('border-primary');
                } else {
                    t.classList.remove('border-primary');
                }
            });
        }
    }

    if (mainImage) {
        mainImage.style.transition = 'opacity 0.15s ease';
        
        if (thumbs.length > 0) {
            if (thumbs[0]) thumbs[0].classList.add('border-primary');
            thumbs.forEach(thumb => {
                thumb.addEventListener('click', e => {
                    e.preventDefault();
                    updateMainImage(thumb.getAttribute('data-image'));
                    thumbs.forEach(t => t.classList.remove('border-primary'));
                    thumb.classList.add('border-primary');
                });
            });
        }

        // Variant Image Switch
        variantRadios.forEach(radio => {
            radio.addEventListener('change', () => {
                const img = radio.getAttribute('data-image');
                if (img) updateMainImage(img, true);
                
                // Also update form hidden input if needed (usually handled by FormData)
                const formImg = document.getElementById('form-image-url');
                if (formImg) formImg.value = img;
            });
        });
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

    if (addToCartForm && addToCartBtn && !addToCartForm.dataset.eventsAttached) {
        addToCartForm.dataset.eventsAttached = "true";
        
        addToCartForm.addEventListener('submit', async function (e) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
            if (addToCartBtn.disabled || addToCartBtn.getAttribute('data-state') === 'success') return;

            const originalHTML = addToCartBtn.innerHTML;
            addToCartBtn.disabled = true;
            addToCartBtn.innerHTML = `
                <i class="fas fa-circle-notch fa-spin"></i>
                <span>Adding&hellip;</span>
            `;

            const engine = window.cartState;
            if (!engine) {
                addToCartBtn.disabled = false;
                addToCartBtn.innerHTML = originalHTML;
                addToCartForm.submit();
                return;
            }

            const result = await engine.addToCart(addToCartForm);

            if (result?.success) {
                addToCartBtn.setAttribute('data-state', 'success');
                addToCartBtn.innerHTML = `
                    <i class="fas fa-check"></i>
                    <span>Show Cart</span>
                `;
                addToCartBtn.classList.remove('bg-primary');
                addToCartBtn.classList.add('bg-secondary', 'text-white');
                addToCartBtn.type = 'button';
                addToCartBtn.disabled = false;
                
                // Important: detach the submit handler logic for redirection
                addToCartBtn.onclick = (event) => {
                    event.preventDefault();
                    window.location.href = '/cart/';
                };

                // Remove the hidden attribute if any
                addToCartBtn.classList.remove('opacity-50', 'cursor-not-allowed');
            } else {
                addToCartBtn.innerHTML = `<span>Try Again</span>`;
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
            addToCartBtn.classList.add('bg-secondary', 'text-white');
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


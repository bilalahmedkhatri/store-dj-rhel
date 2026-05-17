/**
 * Cart Handler v2 — Global AJAX Cart Engine
 * Features:
 *   • BroadcastChannel cross-tab synchronisation
 *   • Toast notification with product preview
 *   • Event delegation (zero inline onclick)
 *   • Animated cart-count badge
 *   • Auto-intercepts all add-to-cart forms
 */
(function () {
    'use strict';

    // ─── CSRF ──────────────────────────────────────────────────────
    function getCSRF() {
        const m = document.cookie.match(/csrftoken=([^;]+)/);
        return m ? decodeURIComponent(m[1]) : '';
    }

    // ─── BroadcastChannel (cross-tab sync) ─────────────────────────
    const channel = (typeof BroadcastChannel !== 'undefined')
        ? new BroadcastChannel('cart_sync')
        : null;

    // ─── Toast ─────────────────────────────────────────────────────
    const Toast = {
        _container: null,

        init() {
            this._container = document.getElementById('toast-container');
        },

        show({ name, image, price, qty = 1 }) {
            if (!this._container) return;
            const el = document.createElement('div');
            el.className = 'cart-toast';
            el.setAttribute('role', 'status');
            el.setAttribute('aria-live', 'polite');
            el.innerHTML = `
                <div class="cart-toast__inner">
                    <div class="cart-toast__icon">
                        <i class="fas fa-check-circle cart-toast__check"></i>
                    </div>
                    <div class="cart-toast__img-wrap">
                        <img src="${image}" alt="" class="cart-toast__img">
                    </div>
                    <div class="cart-toast__body">
                        <p class="cart-toast__label">Added to cart</p>
                        <p class="cart-toast__name">${name}</p>
                        <p class="cart-toast__meta">Qty ${qty} &middot; Rs. ${(price * qty).toFixed(2)}</p>
                    </div>
                    <a href="/cart/" class="cart-toast__cta">View Cart</a>
                    <button class="cart-toast__close" aria-label="Dismiss"><i class="fas fa-times"></i></button>
                </div>
                <div class="cart-toast__progress"></div>
            `;
            this._container.appendChild(el);
            requestAnimationFrame(() => el.classList.add('cart-toast--visible'));

            const timer = setTimeout(() => this._dismiss(el), 4500);
            el.querySelector('.cart-toast__close').addEventListener('click', () => {
                clearTimeout(timer);
                this._dismiss(el);
            });
        },

        _dismiss(el) {
            el.classList.remove('cart-toast--visible');
            el.addEventListener('transitionend', () => el.remove(), { once: true });
        }
    };

    // ─── Cart State ────────────────────────────────────────────────
    window.cartState = {
        items: [],

        setItems(items, { broadcast = true, toast = null } = {}) {
            this.items = Array.isArray(items) ? items : [];
            this._render();
            document.dispatchEvent(new CustomEvent('cart:updated', { detail: { items: this.items } }));
            if (broadcast && channel) {
                channel.postMessage({ type: 'CART_UPDATE', items: this.items });
            }
            if (toast) {
                Toast.show(toast);
            }
        },

        get subtotal() {
            return this.items.reduce((t, i) => t + (parseFloat(i.price) || 0) * (parseInt(i.quantity) || 1), 0);
        },

        get totalItems() {
            return this.items.reduce((t, i) => t + (parseInt(i.quantity) || 1), 0);
        },

        async addToCart(form) {
            const formData    = new FormData(form);
            const name  = formData.get('name')      || 'Item';
            const image = formData.get('image_url') || '';
            const price = parseFloat(formData.get('price'))   || 0;
            const qty   = parseInt(formData.get('quantity'))  || 1;

            // ① Optimistic badge bump — instant feedback
            const badge = document.getElementById('mini-cart-count');
            if (badge) {
                badge.textContent = (parseInt(badge.textContent) || 0) + qty;
                badge.classList.remove('badge-bounce');
                void badge.offsetWidth;
                badge.classList.add('badge-bounce');
            }

            // ② Show toast immediately — no waiting for network
            Toast.show({ name, image, price, qty });

            // ③ Fetch & sync real state
            try {
                const res  = await fetch(form.action, {
                    method: 'POST',
                    body: formData,
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                const data = await res.json();
                if (data.success) {
                    // setItems with no toast (already shown)
                    this.setItems(data.items, { broadcast: true });
                } else {
                    this._render(); // revert optimistic badge
                }
                return data;
            } catch (err) {
                console.error('[cart] addToCart:', err);
                this._render();
                return { success: false };
            }
        },

        async removeItem(slug) {
            const body = new URLSearchParams({ csrfmiddlewaretoken: getCSRF() });
            try {
                const res = await fetch(`/cart/remove/${slug}/`, {
                    method: 'POST',
                    body,
                    headers: { 'X-Requested-With': 'XMLHttpRequest' }
                });
                const data = await res.json();
                if (data.success) {
                    this.setItems(data.items, { broadcast: true });
                }
            } catch (err) {
                console.error('[cart] removeItem:', err);
            }
        },

        _render() {
            const container    = document.getElementById('mini-cart-items');
            const emptyEl      = document.getElementById('mini-cart-empty');
            const countBadge   = document.getElementById('mini-cart-count');
            const itemsLabel   = document.getElementById('mini-cart-items-count');
            const subtotalEl   = document.getElementById('mini-cart-subtotal');

            if (!container) return;

            container.innerHTML = '';

            if (this.items.length === 0) {
                emptyEl?.classList.remove('hidden');
            } else {
                emptyEl?.classList.add('hidden');
                this.items.forEach(item => {
                    const div = document.createElement('div');
                    div.className = 'mini-cart-item flex items-center gap-3 p-4 hover:bg-gray-50 transition-colors';
                    div.dataset.slug = item.slug;
                    div.innerHTML = `
                        <img src="${item.image}" alt="${item.name}"
                             class="w-14 h-14 rounded-xl object-cover flex-shrink-0 shadow-sm bg-gray-100">
                        <div class="flex-1 min-w-0">
                            <p class="text-sm font-semibold text-gray-900 truncate">${item.name}</p>
                            <p class="text-xs text-gray-400 mt-0.5">Qty: ${item.quantity}</p>
                            <p class="text-sm font-bold text-gray-900 mt-0.5">Rs. ${(parseFloat(item.price) * parseInt(item.quantity)).toFixed(2)}</p>
                        </div>
                        <button class="mini-cart-remove flex-shrink-0 text-gray-300 hover:text-red-500 transition-colors p-1.5 rounded-lg hover:bg-red-50"
                                data-slug="${item.slug}" aria-label="Remove ${item.name}">
                            <i class="fas fa-trash-alt" style="font-size: 14px;"></i>
                        </button>
                    `;
                    container.appendChild(div);
                });
            }

            // Animate badge
            if (countBadge) {
                const newCount = String(this.totalItems);
                if (countBadge.textContent !== newCount) {
                    countBadge.textContent = newCount;
                    countBadge.classList.remove('badge-bounce');
                    void countBadge.offsetWidth; // reflow to restart animation
                    countBadge.classList.add('badge-bounce');
                }
            }
            if (itemsLabel) itemsLabel.textContent = this.items.length;
            if (subtotalEl) subtotalEl.textContent = 'Rs. ' + this.subtotal.toFixed(2);
        }
    };

    // ─── Event Delegation: mini-cart remove buttons ────────────────
    document.addEventListener('click', e => {
        const btn = e.target.closest('.mini-cart-remove');
        if (btn) {
            e.preventDefault();
            window.cartState.removeItem(btn.dataset.slug);
        }
    });

    // ─── DOMContentLoaded ──────────────────────────────────────────
    document.addEventListener('DOMContentLoaded', () => {
        Toast.init();

        // Mini-cart toggle
        const toggleBtn  = document.getElementById('mini-cart-toggle');
        const dropdown   = document.getElementById('mini-cart-dropdown');
        if (toggleBtn && dropdown) {
            toggleBtn.addEventListener('click', e => {
                e.stopPropagation();
                dropdown.classList.toggle('hidden');
            });
            document.addEventListener('click', e => {
                if (!dropdown.contains(e.target) && !toggleBtn.contains(e.target)) {
                    dropdown.classList.add('hidden');
                }
            });
        }

        // Global intercept: add-to-cart forms on listing pages
        // NOTE: id="add-to-cart-form" is handled exclusively by product-page.js
        document.addEventListener('submit', e => {
            const form = e.target;
            if (!form.action?.includes('/cart/add/')) return;
            if (form.id === 'add-to-cart-form') return; // product-page.js owns this
            e.preventDefault();
            window.cartState.addToCart(form);
        });

        // Hydrate from server-rendered cart data
        const dataEl = document.getElementById('cart-data');
        if (dataEl) {
            try {
                const items = JSON.parse(dataEl.textContent);
                if (Array.isArray(items)) {
                    window.cartState.setItems(items, { broadcast: false });
                }
            } catch { /* non-critical */ }
        }
    });

    // ─── Cross-tab sync ────────────────────────────────────────────
    if (channel) {
        channel.onmessage = ({ data }) => {
            if (data?.type === 'CART_UPDATE') {
                window.cartState.setItems(data.items, { broadcast: false });
            }
        };
    }
})();

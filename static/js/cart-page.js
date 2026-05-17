/**
 * Cart Page Manager - Handles quantity updates and row deletions on /cart/
 */

(function () {
    // Helper to get CSRF token from cookie
    function getCSRFToken() {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 10) === ('csrftoken=')) {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrfToken = getCSRFToken();

    function getRows() {
        return document.querySelectorAll("[data-cart-row]");
    }

    function parseMoney(value) {
        return Number.parseFloat(value) || 0;
    }

    function formatMoney(value) {
        return "Rs. " + value.toFixed(2);
    }

    function updateEmptyState() {
        const rows = getRows();
        const emptyBlock = document.getElementById("cart-empty-state");
        const cartGrid = document.querySelector("[data-cart-grid]");

        if (rows.length === 0) {
            if (emptyBlock) emptyBlock.classList.remove("hidden");
            if (cartGrid) cartGrid.classList.add("hidden");
        } else {
            if (emptyBlock) emptyBlock.classList.add("hidden");
            if (cartGrid) cartGrid.classList.remove("hidden");
        }
    }

    let isRecalcing = false;
    function recalcSummary(shouldSyncGlobal = true) {
        if (isRecalcing) return;
        isRecalcing = true;

        let subtotal = 0;
        let itemsCount = 0;

        getRows().forEach((row) => {
            const price = parseMoney(row.dataset.price);
            const qtyEl = row.querySelector("[data-item-qty]");
            if (!qtyEl) return;
            const qty = parseInt(qtyEl.textContent) || 1;
            console.log('quantity:', qty);
            console.log('price:', price);
            console.log('total:', price * qty);
            console.log('subtotal:', subtotal);
            console.log('itemsCount:', itemsCount);

            subtotal += price * qty;
            itemsCount += qty;
        });

        const shipping = subtotal > 0 && subtotal < 500 ? 15 : 0;
        const tax = subtotal * 0.08;
        const total = subtotal + shipping + tax;
        const remaining = Math.max(0, 500 - subtotal);

        // ✅ Update UI safely (only if exists)
        const setText = (id, value) => {
            const el = document.getElementById(id);
            if (el) el.textContent = value;
        };

        setText("summary-subtotal", formatMoney(subtotal));
        setText("summary-shipping", shipping === 0 ? "Free" : formatMoney(shipping));
        setText("summary-tax", formatMoney(tax));
        setText("summary-total", formatMoney(total));

        const freeNote = document.getElementById("free-shipping-note");
        if (freeNote) {
            if (shipping === 0 || subtotal === 0) {
                freeNote.classList.add("hidden");
            } else {
                freeNote.classList.remove("hidden");
                freeNote.textContent = `Add ${formatMoney(remaining)} more for free shipping.`;
            }
        }

        const countEl = document.getElementById("cart-items-count");
        if (countEl) {
            countEl.textContent = `${itemsCount} item${itemsCount === 1 ? "" : "s"} in your cart`;
        }

        // 🔥 Sync Mini Cart (if exists)
        if (shouldSyncGlobal && window.cartState) {
            const items = Array.from(getRows()).map(row => ({
                slug: row.dataset.slug,
                name: row.querySelector("h3")?.textContent || "",
                price: parseMoney(row.dataset.price),
                quantity: parseInt(row.querySelector("[data-item-qty]").textContent),
                image: row.querySelector("img")?.src || ""
            }));

            window.cartState.setItems(items);
        }

        updateEmptyState();
        isRecalcing = false;
    }

    // 🔥 Debounce backend sync
    let timeout = null;
    function debounceSync(fn, delay = 400) {
        clearTimeout(timeout);
        timeout = setTimeout(fn, delay);
    }

    async function syncQuantity(row, quantity, oldQty) {
        if (!row.dataset.updateUrl) return;

        debounceSync(async () => {
            try {
                const body = new URLSearchParams();
                body.set("quantity", quantity);

                await fetch(row.dataset.updateUrl, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded",
                        "X-CSRFToken": csrfToken,
                        "X-Requested-With": "XMLHttpRequest",
                    },
                    body: body.toString(),
                });
            } catch (error) {
                // rollback UI
                const qtyEl = row.querySelector("[data-item-qty]");
                if (qtyEl) qtyEl.textContent = oldQty;
                recalcSummary();
            }
        });
    }

    function attachEvents(row) {
        if (row.dataset.eventsAttached) return;
        row.dataset.eventsAttached = "true";

        const qtyEl = row.querySelector("[data-item-qty]");
        const totalEl = row.querySelector("[data-item-total]");
        const minusBtn = row.querySelector('[data-qty-btn="decrease"]');
        const plusBtn = row.querySelector('[data-qty-btn="increase"]');
        const removeBtn = row.querySelector("[data-remove-btn]");
        const price = parseMoney(row.dataset.price);

        function updateUI(qty) {
            if (qtyEl) qtyEl.textContent = qty;
            if (totalEl) totalEl.textContent = formatMoney(price * qty);
            if (minusBtn) minusBtn.disabled = qty <= 1;
            recalcSummary();
        }

        if (minusBtn) {
            minusBtn.addEventListener("click", (e) => {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                let current = parseInt(qtyEl.textContent) || 1;
                if (current <= 1) return;

                let newQty = current - 1;
                updateUI(newQty);
                syncQuantity(row, newQty, current);
            });
        }

        if (plusBtn) {
            plusBtn.addEventListener("click", (e) => {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                let current = parseInt(qtyEl.textContent) || 1;
                let newQty = current + 1;

                updateUI(newQty);
                syncQuantity(row, newQty, current);
            });
        }

        if (removeBtn) {
            removeBtn.addEventListener("click", async (e) => {
                e.preventDefault();
                e.stopPropagation();
                e.stopImmediatePropagation();
                const slug = row.dataset.slug;
                row.remove();
                recalcSummary();

                // Call global remove to keep state in sync
                if (window.cartState) {
                    window.cartState.removeItem(slug);
                }
            });
        }
    }

    // 🔥 INIT
    document.addEventListener("DOMContentLoaded", () => {
        getRows().forEach((row) => attachEvents(row));
        recalcSummary(); // 🔥 important on load
    });

    // 🔥 SYNC FROM GLOBAL (if mini-cart removes item)
    document.addEventListener('cart:updated', (e) => {
        const globalItems = e.detail.items;
        const currentRows = getRows();

        if (globalItems.length < currentRows.length) {
            const globalSlugs = globalItems.map(item => item.slug);
            currentRows.forEach(row => {
                if (!globalSlugs.includes(row.dataset.slug)) {
                    row.remove();
                }
            });
            recalcSummary(false); // don't sync back to global
        }
    });

})();

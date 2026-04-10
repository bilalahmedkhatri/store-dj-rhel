/**
 * Checkout Stepper — Multi-step form navigation + validation
 * Steps: 1 = Contact  2 = Shipping  3 = Payment  4 = Review
 */
(function () {
    'use strict';

    let currentStep = 1;
    const TOTAL_STEPS = 4;

    // ─── Validation rules per step ─────────────────────────────────
    const STEP_FIELDS = {
        1: [
            { id: 'email',      errorId: 'email-error',      test: v => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) },
            { id: 'first-name', errorId: 'first-name-error', test: v => v.trim().length > 0 },
            { id: 'last-name',  errorId: 'last-name-error',  test: v => v.trim().length > 0 },
            { id: 'address',    errorId: 'address-error',    test: v => v.trim().length > 0 },
            { id: 'city',       errorId: 'city-error',       test: v => v.trim().length > 0 },
            { id: 'postal',     errorId: 'postal-error',     test: v => v.trim().length >= 3 },
            { id: 'country',    errorId: 'country-error',    test: v => v !== '' },
        ],
        2: [],  // Shipping: radio always has a default, no extra validation needed
        3: [],  // Payment validation: applied dynamically (see below)
        4: [
            { id: 'agree-terms', errorId: 'terms-error', test: (_, el) => el.checked, isCheckbox: true },
        ],
    };

    // ─── Helpers ───────────────────────────────────────────────────
    function $(id) { return document.getElementById(id); }

    function showError(errorId) {
        const el = $(errorId);
        if (el) el.classList.add('visible');
    }
    function hideError(errorId) {
        const el = $(errorId);
        if (el) el.classList.remove('visible');
    }
    function markInputError(inputId, hasError) {
        const el = $(inputId);
        if (!el) return;
        if (hasError) {
            el.classList.add('input-error');
        } else {
            el.classList.remove('input-error');
        }
    }

    // ─── Validate a step ───────────────────────────────────────────
    function validateStep(step) {
        let valid = true;
        const fields = STEP_FIELDS[step] || [];

        // Dynamic payment validation on step 3
        if (step === 3) {
            const paymentMethod = document.querySelector('[name="payment"]:checked')?.value;
            if (paymentMethod === 'card') {
                const cardFields = [
                    { id: 'card-number', errorId: 'card-number-error', test: v => /^\d[\d\s]{13,17}$/.test(v.replace(/\s/g, '').padEnd(16, '0')) || v.replace(/\D/g, '').length === 16 },
                    { id: 'card-name',   errorId: 'card-name-error',   test: v => v.trim().length > 1 },
                    { id: 'card-expiry', errorId: 'card-expiry-error', test: v => /^\d{2}[\s/]+\d{2}$/.test(v) },
                    { id: 'card-cvc',    errorId: 'card-cvc-error',    test: v => /^\d{3,4}$/.test(v) },
                ];
                cardFields.forEach(({ id, errorId, test }) => {
                    const el = $(id);
                    if (!el) return;
                    const ok = test(el.value);
                    markInputError(id, !ok);
                    if (ok) hideError(errorId); else { showError(errorId); valid = false; }
                });
            }
            return valid;
        }

        fields.forEach(({ id, errorId, test, isCheckbox }) => {
            const el = $(id);
            if (!el) return;
            const ok = isCheckbox ? test(null, el) : test(el.value);
            markInputError(id, !ok);
            if (ok) hideError(errorId); else { showError(errorId); valid = false; }
        });

        return valid;
    }

    // ─── Stepper UI ────────────────────────────────────────────────
    function updateStepper(newStep) {
        document.querySelectorAll('.checkout-step').forEach(stepEl => {
            const n = parseInt(stepEl.dataset.step);
            stepEl.classList.remove('active', 'completed');
            if (n === newStep) stepEl.classList.add('active');
            else if (n < newStep) stepEl.classList.add('completed');

            // Checkmark for completed circles
            const circle = stepEl.querySelector('.step-circle');
            if (!circle) return;
            if (n < newStep) {
                circle.innerHTML = `<i class="fas fa-check" style="font-size:10px"></i>`;
            } else {
                circle.textContent = n;
            }
        });

        // Connectors
        for (let i = 1; i < TOTAL_STEPS; i++) {
            const conn = $(`connector-${i}-${i + 1}`);
            if (conn) {
                if (i < newStep) conn.classList.add('completed');
                else             conn.classList.remove('completed');
            }
        }
    }

    function showPanel(step) {
        for (let i = 1; i <= TOTAL_STEPS; i++) {
            const panel = $(`panel-${i}`);
            if (!panel) continue;
            panel.classList.remove('panel-active');
        }
        const active = $(`panel-${step}`);
        if (active) {
            active.classList.add('panel-active');
            active.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }

    function goToStep(step) {
        currentStep = step;
        updateStepper(step);
        showPanel(step);
        populateReview();
    }

    // ─── Review section population ─────────────────────────────────
    function populateReview() {
        if (currentStep !== 4) return;

        const email     = $('email')?.value      || '—';
        const firstName = $('first-name')?.value || '';
        const lastName  = $('last-name')?.value  || '';
        const phone     = $('phone')?.value      || '';
        const address   = $('address')?.value    || '';
        const city      = $('city')?.value        || '';
        const postal    = $('postal')?.value      || '';

        const reviewEmail   = $('review-email');
        const reviewName    = $('review-name');
        const reviewPhone   = $('review-phone');
        const reviewAddress = $('review-address');
        const reviewShip    = $('review-shipping');

        if (reviewEmail)   reviewEmail.textContent   = email;
        if (reviewName)    reviewName.textContent     = `${firstName} ${lastName}`.trim() || '—';
        if (reviewPhone) {
            reviewPhone.textContent = phone || '—';
        }
        const phoneWrap = $('review-phone-wrap');
        if (phoneWrap) phoneWrap.style.display = phone ? '' : 'none';

        if (reviewAddress) reviewAddress.textContent = [address, city, postal].filter(Boolean).join(', ') || '—';


        const selectedShipping = document.querySelector('[name="shipping_method"]:checked');
        if (reviewShip && selectedShipping) {
            const label = selectedShipping.closest('label')?.querySelector('p.text-sm.font-semibold')?.childNodes[0]?.textContent?.trim();
            reviewShip.textContent = label || 'Standard';
        }
    }

    // ─── Card number formatting ────────────────────────────────────
    function formatCardNumber(input) {
        let val = input.value.replace(/\D/g, '').slice(0, 16);
        input.value = val.replace(/(.{4})/g, '$1 ').trim();
    }

    function formatExpiry(input) {
        let val = input.value.replace(/\D/g, '').slice(0, 4);
        if (val.length >= 3) val = val.slice(0, 2) + ' / ' + val.slice(2);
        input.value = val;
    }

    // ─── Shipping method visual state ──────────────────────────────
    function setupShippingOptions() {
        document.querySelectorAll('.shipping-option').forEach(label => {
            const radio = label.querySelector('input[type="radio"]');
            const dot   = label.querySelector('.method-inner');
            if (!radio || !dot) return;

            function refresh() {
                document.querySelectorAll('.shipping-option .method-inner').forEach(d => {
                    d.style.opacity = '0';
                });
                const checked = label.querySelector('input:checked');
                if (checked) dot.style.opacity = '1';
            }

            radio.addEventListener('change', refresh);
            if (radio.checked) dot.style.opacity = '1';
        });
    }

    // ─── Payment method toggle ─────────────────────────────────────
    function setupPaymentToggle() {
        const cardFields = $('card-fields');
        document.querySelectorAll('[name="payment"]').forEach(radio => {
            radio.addEventListener('change', () => {
                if (cardFields) {
                    cardFields.style.display = radio.value === 'card' ? '' : 'none';
                }
            });
        });
    }

    // ─── Coupon input (cosmetic demo) ──────────────────────────────
    function setupCoupon() {
        const btn     = $('apply-coupon');
        const input   = $('coupon-input');
        const success = $('coupon-success');
        if (!btn || !input) return;

        btn.addEventListener('click', () => {
            const code = input.value.trim().toUpperCase();
            if (code === 'SAVE10' || code === 'WELCOME') {
                if (success) {
                    success.textContent = `✓ Coupon "${code}" applied! You saved $5.00.`;
                    success.classList.remove('hidden');
                }
                input.disabled = true;
                btn.textContent = '✓ Applied';
                btn.disabled    = true;
            } else if (code !== '') {
                input.classList.add('input-error');
                setTimeout(() => input.classList.remove('input-error'), 2000);
            }
        });
    }

    // ─── Init ──────────────────────────────────────────────────────
    document.addEventListener('DOMContentLoaded', () => {
        // "Continue" buttons
        document.querySelectorAll('.btn-next').forEach(btn => {
            btn.addEventListener('click', () => {
                const target = parseInt(btn.dataset.target);
                if (!validateStep(currentStep)) return;
                goToStep(target);
            });
        });

        // "Back" buttons
        document.querySelectorAll('.btn-back').forEach(btn => {
            btn.addEventListener('click', () => {
                const target = parseInt(btn.dataset.target);
                goToStep(target);
            });
        });

        // Stepper circle click to go back
        document.querySelectorAll('.checkout-step').forEach(stepEl => {
            const n = parseInt(stepEl.dataset.step);
            stepEl.querySelector('.step-circle')?.addEventListener('click', () => {
                if (n < currentStep) goToStep(n);
            });
        });

        // Card formatting
        const cardNum    = $('card-number');
        const cardExpiry = $('card-expiry');
        if (cardNum)    cardNum.addEventListener('input',    () => formatCardNumber(cardNum));
        if (cardExpiry) cardExpiry.addEventListener('input', () => formatExpiry(cardExpiry));

        // Inline validation: clear errors on input
        document.querySelectorAll('.checkout-input').forEach(input => {
            input.addEventListener('input', () => {
                input.classList.remove('input-error');
                const errorEl = document.getElementById(`${input.id}-error`);
                if (errorEl) errorEl.classList.remove('visible');
            });
        });

        // Submit: validate step 4
        const form = $('checkout-form');
        if (form) {
            form.addEventListener('submit', e => {
                if (!validateStep(4)) {
                    e.preventDefault();
                    return;
                }
                // Final loading state
                const btn = $('place-order-btn');
                if (btn) {
                    btn.disabled = true;
                    btn.innerHTML = `
                        <i class="fas fa-circle-notch fa-spin text-lg"></i>
                        <span>Placing Order...</span>
                    `;
                }

            });
        }

        setupShippingOptions();
        setupPaymentToggle();
        setupCoupon();
        updateStepper(1);
    });
})();

from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from .cart_utils import CART_SESSION_KEY, build_cart_context

def checkout_view(request):
    if request.method == "POST":
        request.session[CART_SESSION_KEY] = []
        request.session.modified = True
        # In a real scenario, we'd redirect to the payment gateway or success page
        # For now, let's redirect to payment success
        return redirect("payment_success")

    context = build_cart_context(request)
    return render(request, "landing/checkout.html", context)

def payment_success_view(request):
    # In a real app, we'd fetch transaction details from session or DB
    context = {
        'transaction_id': 'PF-TXN-12345',
        'amount': '2,500.00',
        'timestamp': '2026-04-12 14:30:00',
    }
    return render(request, "landing/payment_success.html", context)

def payment_failed_view(request):
    context = {
        'reason': 'Insufficient funds or transaction declined by bank.',
        'auto_refund_notice': 'If amount was deducted, it will be auto-refunded within 7 days.',
    }
    return render(request, "landing/payment_failed.html", context)

def payment_pending_view(request):
    context = {
        'transaction_ref': 'REF-987654',
    }
    return render(request, "landing/payment_pending.html", context)

def receipt_view(request, transaction_id):
    # In a real app, we'd fetch order details by transaction_id
    context = {
        'transaction_id': transaction_id,
        'amount': '2,500.00',
        'payer_name': 'Bilal Ahmed Khatri',
        'timestamp': '2026-04-12 14:30:00',
    }
    return render(request, "landing/receipt.html", context)

from django.contrib import messages
from django.shortcuts import redirect, render

from .cart_utils import CART_SESSION_KEY, build_cart_context

def checkout_view(request):
    if request.method == "POST":
        request.session[CART_SESSION_KEY] = []
        request.session.modified = True
        messages.success(request, "Order placed successfully. Thank you for your purchase!")
        return redirect("index")

    context = build_cart_context(request)
    return render(request, "landing/checkout.html", context)

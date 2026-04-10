from django.http import JsonResponse
from django.shortcuts import redirect, render
from .cart_utils import (
    add_to_cart_session,
    build_cart_context,
    remove_from_cart_session,
    update_quantity_session,
)
from .mock_data import get_mock_cart_context

def cart_view(request):
    context = build_cart_context(request)
    if not context["cart_items"]:
        context = get_mock_cart_context()
    return render(request, "landing/cart.html", context)


def add_to_cart_view(request):
    if request.method == "POST":
        add_to_cart_session(
            request,
            {
                "slug": request.POST.get("slug"),
                "name": request.POST.get("name"),
                "image_url": request.POST.get("image_url"),
                "price": request.POST.get("price", 0),
                "variant": request.POST.get("variant", "Standard"),
                "quantity": request.POST.get("quantity", 1),
            },
        )
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = build_cart_context(request)
            # Format items for JS engine
            js_items = [{
                "slug": item["slug"],
                "name": item["product"]["name"],
                "image": item["product"]["image"]["url"],
                "price": item["price"],
                "quantity": item["quantity"]
            } for item in context["cart_items"]]
            
            return JsonResponse({
                "success": True, 
                "items": js_items,
                "total_items": context["cart_count"],
                "subtotal": context["subtotal"]
            })
            
    return redirect(request.POST.get("next") or "cart")


def cart_update_view(request, slug):
    if request.method == "POST":
        update_quantity_session(request, slug=slug, quantity=int(request.POST.get("quantity", 1)))
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = build_cart_context(request)
            js_items = [{
                "slug": item["slug"],
                "name": item["product"]["name"],
                "image": item["product"]["image"]["url"],
                "price": item["price"],
                "quantity": item["quantity"]
            } for item in context["cart_items"]]
            return JsonResponse({"success": True, "items": js_items, "subtotal": context["subtotal"]})
            
    return redirect("cart")


def cart_remove_view(request, slug):
    if request.method == "POST":
        remove_from_cart_session(request, slug=slug)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            context = build_cart_context(request)
            js_items = [{
                "slug": item["slug"],
                "name": item["product"]["name"],
                "image": item["product"]["image"]["url"],
                "price": item["price"],
                "quantity": item["quantity"]
            } for item in context["cart_items"]]
            return JsonResponse({"success": True, "items": js_items, "subtotal": context["subtotal"]})
            
    return redirect("cart")
import json
from .views.cart_utils import build_cart_context


def cart_processor(request):
    context = build_cart_context(request)
    cart_items = context.get("cart_items", [])
    
    cart_items_json = json.dumps([
        {
            "slug": item["slug"],
            "name": item["product"]["name"],
            "price": float(item["price"]),
            "quantity": item["quantity"],
            "image": item["product"]["image"]["url"]
        }
        for item in cart_items
    ])

    return {
        "header_cart_items": cart_items[:2],
        "header_cart_count": context.get("cart_count", 0),
        "header_cart_total": context.get("total", 0),
        "cart_items_json": cart_items_json,
    }
# # context_processors.py
# from django.utils import translation

# def language_processor(request):
#     return {
#         'current_language': translation.get_language(),
#         'available_languages': ['en', 'ur', 'ar'],  # Add your languages
#     }
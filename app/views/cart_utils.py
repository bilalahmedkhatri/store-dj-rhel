from __future__ import annotations

from typing import Any
from django.utils.text import slugify


CART_SESSION_KEY = "store_cart"


def _default_item(payload: dict[str, Any]) -> dict[str, Any]:
    qty = int(payload.get("quantity", 1))
    price = float(payload.get("price", 0))
    raw_slug = (payload.get("slug") or "").strip()
    name = payload.get("name", "Product")
    safe_slug = raw_slug or slugify(name) or f"item-{abs(hash(name)) % 1000000}"
    return {
        "slug": safe_slug,
        "name": name,
        "image_url": payload.get("image_url", "/static/images/products/product.jpg"),
        "variant": payload.get("variant", "Standard"),
        "price": round(price, 2),
        "quantity": max(1, qty),
    }


def get_cart(request) -> list[dict[str, Any]]:
    cart = request.session.get(CART_SESSION_KEY, [])
    if not isinstance(cart, list):
        cart = []
    return cart


def save_cart(request, cart: list[dict[str, Any]]) -> None:
    request.session[CART_SESSION_KEY] = cart
    request.session.modified = True


def add_to_cart_session(request, payload: dict[str, Any]) -> None:
    cart = get_cart(request)
    item = _default_item(payload)
    for row in cart:
        if row.get("slug") == item["slug"] and row.get("variant") == item["variant"]:
            row["quantity"] = int(row.get("quantity", 1)) + item["quantity"]
            save_cart(request, cart)
            return
    cart.append(item)
    save_cart(request, cart)


def update_quantity_session(request, slug: str, quantity: int) -> None:
    cart = get_cart(request)
    for row in cart:
        if row.get("slug") == slug:
            row["quantity"] = max(1, int(quantity))
            break
    save_cart(request, cart)


def remove_from_cart_session(request, slug: str) -> None:
    cart = [row for row in get_cart(request) if row.get("slug") != slug]
    save_cart(request, cart)


def build_cart_context(request) -> dict[str, Any]:
    cart = get_cart(request)
    cart_items = []
    subtotal = 0.0
    for row in cart:
        row_slug = (row.get("slug") or "").strip() or slugify(row.get("name", "product")) or f"item-{abs(hash(row.get('name', 'product'))) % 1000000}"
        qty = int(row.get("quantity", 1))
        price = float(row.get("price", 0))
        total_price = round(price * qty, 2)
        subtotal += total_price
        cart_items.append(
            {
                "slug": row_slug,
                "product": {
                    "name": row.get("name", "Product"),
                    "image": {"url": row.get("image_url", "/static/images/products/product.jpg")},
                },
                "variant": row.get("variant", "Standard"),
                "quantity": qty,
                "price": price,
                "total_price": total_price,
            }
        )

    shipping = 0.0 if subtotal >= 500 else (15.0 if subtotal > 0 else 0.0)
    tax = round(subtotal * 0.08, 2)
    total = round(subtotal + shipping + tax, 2)
    return {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "shipping": shipping,
        "tax": tax,
        "total": total,
        "amount_to_free_shipping": max(0.0, 500.0 - subtotal),
        "cart_count": sum(item["quantity"] for item in cart_items),
    }

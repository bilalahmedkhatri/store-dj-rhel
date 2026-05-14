import os
from django.conf import settings

FALLBACK_IMAGES = [
    "1.jpg",
    "2.jpg",
    "3.jpg",
    "4.jpg",
    "5.jpg",
    "6.jpg",
    "7.jpg",
    "8.jpg",
    "loewe-1.jpg",
    "loewe-2.jpg",
    "loewe-3.jpg",
    "loewe-4.jpg",
]


def resolve_fallback_image(seed="") -> str:
    """Deterministically pick a fallback image based on seed string."""
    index = abs(hash(seed)) % len(FALLBACK_IMAGES)
    return f"/static/images/products/{FALLBACK_IMAGES[index]}"


def _is_external_url(url):
    return url and "/static/" not in url


def resolve_product_image(variant, product, seed="") -> str:
    if (
        variant
        and variant.featuredassetid
        and _is_external_url(variant.featuredassetid.preview)
    ):
        return variant.featuredassetid.preview
    if (
        product
        and product.featuredassetid
        and _is_external_url(product.featuredassetid.preview)
    ):
        return product.featuredassetid.preview
    return resolve_fallback_image(seed)

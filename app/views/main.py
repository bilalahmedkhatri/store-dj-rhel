import os

from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from django.http import Http404, FileResponse
from django.shortcuts import get_object_or_404, render

from ..models import (
    Collection,
    CollectionTranslation,
    Product,
    ProductTranslation,
    ProductVariant,
    ProductVariantPrice,
    ProductVariantTranslation,
    MerchantProfile,
)
from .image_utils import resolve_fallback_image, resolve_product_image
from .mock_data import get_mock_categories, get_mock_products


@login_required
@user_passes_test(lambda u: u.is_staff)
def serve_merchant_document(request, merchant_id, doc_type):
    merchant = get_object_or_404(MerchantProfile, pk=merchant_id)
    file_field = getattr(merchant, doc_type, None)
    if not file_field or not file_field.name:
        raise Http404("Document not found")
    file_path = file_field.path
    if not os.path.exists(file_path):
        raise Http404("File not found on disk")
    content_type = (
        "application/pdf" if file_path.endswith(".pdf") else "image/jpeg"
    )
    return FileResponse(open(file_path, "rb"), content_type=content_type)

def index(request):
    lang = "en"
    variants = (
        ProductVariant.objects.filter(
            enabled=True,
            deletedat__isnull=True,
            productid__enabled=True,
            productid__deletedat__isnull=True,
        )
        .select_related(
            "productid",
            "productid__featuredassetid",
            "featuredassetid",
        )
        .prefetch_related(
            Prefetch(
                "productid__producttranslation_set",
                ProductTranslation.objects.filter(languagecode=lang),
            ),
            Prefetch(
                "productvarianttranslation_set",
                ProductVariantTranslation.objects.filter(languagecode=lang),
            ),
            "productvariantprice_set",
        )
        .distinct()
        .order_by("id")[:20]
    )

    seen_product_ids = set()
    product_list = []

    for variant in variants:
        product = variant.productid
        if not product or product.id in seen_product_ids:
            continue
        translations = list(variant.productid.producttranslation_set.all())
        if not translations:
            continue
        pt = translations[0]
        seen_product_ids.add(product.id)

        vt_list = list(variant.productvarianttranslation_set.all())
        variant_label = vt_list[0].name if vt_list and vt_list[0].name else ""

        prices = list(variant.productvariantprice_set.all())
        price_cents = prices[0].price if prices else None
        price_display = (
            f"{(price_cents / 100):.2f}" if price_cents is not None else "0.00"
        )

        image_url = resolve_product_image(variant, product, pt.slug)

        product_list.append({
            "name": pt.name,
            "slug": pt.slug,
            "variant_label": variant_label,
            "price": price_display,
            "image_url": image_url,
            "description": pt.description if hasattr(pt, "description") else "",
        })

    if len(product_list) > 10:
        product_list = product_list[:10]

    mock_products = get_mock_products()
    if len(product_list) < 10:
        for mp in mock_products:
            if len(product_list) >= 10:
                break
            if not any(p.get("slug") == mp.get("slug") for p in product_list):
                product_list.append(mp)

    categories = []
    db_categories = list(
        Collection.objects.filter(isprivate=False)
        .prefetch_related(
            Prefetch(
                "collectiontranslation_set",
                CollectionTranslation.objects.filter(languagecode="en"),
            )
        )[:10]
    )
    for category in db_categories:
        translation = next(iter(category.collectiontranslation_set.all()), None)
        cat_name = translation.name if translation else category.get_name("en")
        cat_image = (
            category.featuredassetid.source
            if category.featuredassetid and category.featuredassetid.source
            else resolve_fallback_image(cat_name)
        )
        categories.append({
            "id": category.id,
            "name": cat_name,
            "image_url": cat_image,
            "url": f"/category/{category.id}/",
        })

    mock_categories = get_mock_categories()
    if len(categories) < 4:
        for mc in mock_categories:
            if len(categories) >= 4:
                break
            if not any(c.get("name") == mc.get("name") for c in categories):
                categories.append(mc)

    popular_products = product_list[:5]
    latest_products = product_list[5:10]

    return render(request, "landing/body.html", {
        "products": product_list,
        "popular_products": popular_products,
        "latest_products": latest_products,
        "categories": categories,
    })


def category_list(request):
    categories = []
    for category in (
        Collection.objects.filter(isprivate=False)
        .order_by("position")
        .prefetch_related("collectiontranslation_set")
    ):
        translation = next(iter(category.collectiontranslation_set.all()), None)
        cat_name = translation.name if translation else category.get_name("en")
        cat_image = (
            category.featuredassetid.source
            if category.featuredassetid and category.featuredassetid.source
            else resolve_fallback_image(cat_name)
        )
        categories.append({
            "id": category.id,
            "name": cat_name,
            "image_url": cat_image,
            "url": f"/category/{category.id}/",
        })
    return render(request, "components/banners.html", {"categories": categories})


def category_detail(request, category_id, slug=None):
    lang = "en"
    category = get_object_or_404(
        Collection.objects.filter(isprivate=False), pk=category_id,
    )

    cat_trans = CollectionTranslation.objects.filter(
        baseid=category, languagecode=lang
    ).first()
    if slug and cat_trans and cat_trans.slug != slug:
        raise Http404("Category not found")

    category_name = cat_trans.name if cat_trans else category.get_name(lang)
    category_description = (
        (cat_trans.description or "").strip() if cat_trans else ""
    )

    variants = (
        ProductVariant.objects.filter(
            collectionproductvariantsproductvariant__collectionid=category,
            enabled=True,
            deletedat__isnull=True,
            productid__enabled=True,
            productid__deletedat__isnull=True,
        )
        .select_related(
            "productid",
            "productid__featuredassetid",
            "featuredassetid",
        )
        .prefetch_related(
            Prefetch(
                "productid__producttranslation_set",
                ProductTranslation.objects.filter(languagecode=lang),
            ),
            Prefetch(
                "productvarianttranslation_set",
                ProductVariantTranslation.objects.filter(languagecode=lang),
            ),
            "productvariantprice_set",
        )
        .distinct()
        .order_by("id")
    )

    seen_product_ids = set()
    product_items = []

    for variant in variants:
        product = variant.productid
        if not product or product.id in seen_product_ids:
            continue
        translations = list(variant.productid.producttranslation_set.all())
        if not translations:
            continue
        pt = translations[0]
        seen_product_ids.add(product.id)

        vt_list = list(variant.productvarianttranslation_set.all())
        variant_label = vt_list[0].name if vt_list and vt_list[0].name else ""

        prices = list(variant.productvariantprice_set.all())
        price_cents = prices[0].price if prices else None
        price_display = (
            f"{(price_cents / 100):.2f}" if price_cents is not None else "0.00"
        )

        image_url = resolve_product_image(variant, product, pt.slug)

        product_items.append({
            "name": pt.name,
            "slug": pt.slug,
            "variant_label": variant_label,
            "price": price_display,
            "image_url": image_url,
        })
    if not product_items:
        product_items = get_mock_products()[:6]

    subcategories = []
    for sub in (
        Collection.objects.filter(parentid=category, isprivate=False)
        .order_by("position")
        .prefetch_related(
            Prefetch(
                "collectiontranslation_set",
                CollectionTranslation.objects.filter(languagecode=lang),
            )
        )
    ):
        st_list = list(sub.collectiontranslation_set.all())
        st = st_list[0] if st_list else None
        subcategories.append(
            {
                "id": sub.id,
                "slug": st.slug if st else "",
                "name": st.name if st else sub.get_name(lang),
            }
        )

    return render(
        request,
        "landing/category_detail.html",
        {
            "category": category,
            "category_name": category_name,
            "category_description": category_description,
            "product_items": product_items,
            "product_count": len(product_items),
            "subcategories": subcategories,
        },
    )


def all_products(request):
    variants = ProductVariant.objects.filter(
        enabled=True
    ).prefetch_related(
        "productvarianttranslation_set",
        "product__producttranslation_set",
        "productvariantprice_set"
    )

    product_items = []
    for variant in variants:
        try:
            variant_trans = ProductVariantTranslation.objects.filter(
                baseid=variant, languagecode="en"
            ).first()
            product_trans = ProductTranslation.objects.filter(
                baseid=variant.productid, languagecode="en"
            ).first()
            if not product_trans:
                continue
            price_obj = ProductVariantPrice.objects.filter(
                variantid=variant
            ).first()
            price = price_obj.price / 100 if price_obj else 0.0
            image_url = resolve_product_image(
                variant, variant.productid, product_trans.slug
            )
            product_items.append({
                "name": product_trans.name,
                "slug": product_trans.slug,
                "variant_label": variant_trans.name if variant_trans else "",
                "price": f"{price:.2f}",
                "image_url": image_url,
            })
        except Exception:
            continue

    if not product_items:
        product_items = get_mock_products()

    return render(request, "landing/all_products.html", {"products": product_items})


def load_more_products(request):
    try:
        offset = int(request.GET.get("offset", 10))
        limit = int(request.GET.get("limit", 10))
    except ValueError:
        offset, limit = 10, 10

    lang = "en"
    variants = (
        ProductVariant.objects.filter(
            enabled=True,
            deletedat__isnull=True,
            productid__enabled=True,
            productid__deletedat__isnull=True,
        )
        .select_related("productid", "productid__featuredassetid", "featuredassetid")
        .prefetch_related(
            Prefetch(
                "productid__producttranslation_set",
                ProductTranslation.objects.filter(languagecode=lang),
            ),
            Prefetch(
                "productvarianttranslation_set",
                ProductVariantTranslation.objects.filter(languagecode=lang),
            ),
            "productvariantprice_set",
        )
        .distinct()
        .order_by("id")[offset:offset + limit]
    )

    product_list = []
    seen_product_ids = set()

    for variant in variants:
        product = variant.productid
        if not product or product.id in seen_product_ids:
            continue
        translations = list(variant.productid.producttranslation_set.all())
        if not translations:
            continue
        pt = translations[0]
        seen_product_ids.add(product.id)

        vt_list = list(variant.productvarianttranslation_set.all())
        variant_label = vt_list[0].name if vt_list and vt_list[0].name else ""

        prices = list(variant.productvariantprice_set.all())
        price_cents = prices[0].price if prices else None
        price_display = (
            f"{(price_cents / 100):.2f}" if price_cents is not None else "0.00"
        )

        image_url = resolve_product_image(variant, product, pt.slug)

        product_list.append({
            "name": pt.name,
            "slug": pt.slug,
            "variant_label": variant_label,
            "price": price_display,
            "image_url": image_url,
            "description": pt.description if hasattr(pt, "description") else "",
        })

    return render(
        request, "components/product_grid_items.html", {"products": product_list}
    )

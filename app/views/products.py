from django.http import Http404
from django.shortcuts import render

from ..models import (
    Asset,
    Collection,
    CollectionTranslation,
    FacetValue,
    FacetValueTranslation,
    Product,
    ProductAsset,
    ProductFacetValuesFacetValue,
    ProductOption,
    ProductOptionTranslation,
    ProductTranslation,
    ProductVariant,
    ProductVariantOptionsProductOption,
    ProductVariantPrice,
)
from .image_utils import resolve_fallback_image, resolve_product_image
from .mock_data import get_mock_products, get_mock_shop_filters


def products_view(request):
    products = Product.objects.filter(enabled=True)
    product_list = []

    for product in products:
        try:
            translation = ProductTranslation.objects.filter(
                baseid=product, languagecode="en"
            ).first()
            if not translation:
                continue
            variant = ProductVariant.objects.filter(
                productid=product, enabled=True
            ).first()
            if not variant:
                continue
            price_obj = ProductVariantPrice.objects.filter(
                variantid=variant
            ).first()
            price = price_obj.price / 100 if price_obj else 0.0
            image_url = resolve_product_image(variant, product, translation.slug)
            product_list.append({
                "name": translation.name,
                "description": translation.description,
                "price": f"{price:.2f}",
                "image_url": image_url,
                "slug": translation.slug,
            })
        except Exception as e:
            print(f"Error processing product {product.id}: {e}")
            continue
            
    filters = {
        "categories": [],
        "facet_groups": {},
        "option_groups": {},
        "price_min": 0.0,
        "price_max": 0.0,
    }

    category_names = []
    for category in (
        Collection.objects.filter(isprivate=False)
        .order_by("position")[:12]
    ):
        trans = CollectionTranslation.objects.filter(
            baseid=category, languagecode="en"
        ).first()
        if trans and trans.name:
            category_names.append(trans.name)
    filters["categories"] = category_names

    facet_groups = {}
    facet_links = (
        ProductFacetValuesFacetValue.objects
        .filter(productid__in=products[:100])
        .select_related("facetvalueid__facetid")
    )
    for link in facet_links:
        facet = link.facetvalueid.facetid
        if not facet:
            continue
        facet_key = facet.code.lower()
        trans = FacetValueTranslation.objects.filter(
            baseid=link.facetvalueid, languagecode="en"
        ).first()
        if not trans or not trans.name:
            continue
        facet_groups.setdefault(facet_key, set()).add(trans.name)
    filters["facet_groups"] = {
        k: sorted(list(v))[:10] for k, v in facet_groups.items()
    }

    option_groups = {}
    variant_ids = (
        ProductVariant.objects
        .filter(productid__in=products[:100], enabled=True)
        .values_list("id", flat=True)
    )
    variant_options = (
        ProductVariantOptionsProductOption.objects
        .filter(productvariantid__in=variant_ids)
        .select_related("productoptionid__groupid")
    )
    for vo in variant_options:
        if not vo.productoptionid or not vo.productoptionid.groupid:
            continue
        group_key = vo.productoptionid.groupid.code.lower()
        trans = ProductOptionTranslation.objects.filter(
            baseid=vo.productoptionid, languagecode="en"
        ).first()
        if not trans or not trans.name:
            continue
        option_groups.setdefault(group_key, set()).add(trans.name)
    filters["option_groups"] = {
        k: sorted(list(v))[:10] for k, v in option_groups.items()
    }

    prices = ProductVariantPrice.objects.filter(
        variantid__productid__in=products
    ).values_list("price", flat=True)
    price_values = [p / 100 for p in prices if p is not None]
    if price_values:
        filters["price_min"] = float(min(price_values))
        filters["price_max"] = float(max(price_values))

    if not product_list:
        product_list = get_mock_products()
    if (
        not filters["categories"]
        and not filters["facet_groups"]
        and not filters["option_groups"]
    ):
        filters = get_mock_shop_filters()

    return render(request, "landing/products.html", {
        "products": product_list,
        "filters": filters,
    })


def product_detail_view(request, slug):
    translation = ProductTranslation.objects.filter(
        slug=slug, languagecode="en"
    ).first()
    if not translation:
        mock = next(
            (item for item in get_mock_products() if item["slug"] == slug),
            None,
        )
        if not mock:
            raise Http404("Product not found")
        fallback_img = resolve_fallback_image(slug)
        context = {
            "product": None,
            "name": mock["name"],
            "description": mock["description"],
            "slug": mock["slug"],
            "images": [fallback_img],
            "main_image": fallback_img,
            "min_price": mock["price"],
            "max_price": mock["price"],
            "price_display": mock["price"],
            "facets": [
                {"group": "material", "name": "Premium build"},
                {"group": "warranty", "name": "1 year"},
            ],
            "options": [
                {"group": "Color", "name": "Black", "id": 1},
                {"group": "Color", "name": "Silver", "id": 2},
            ],
            "detailed_variants": [{
                "id": 1,
                "sku": "MOCK-001",
                "price": mock["price"],
                "options": mock.get("variant_label", "Standard"),
                "image": fallback_img,
            }],
            "variants_count": 1,
        }
        return render(request, "landing/product.html", context)
    product = translation.baseid

    variants = ProductVariant.objects.filter(
        productid=product, enabled=True
    )

    product_assets = ProductAsset.objects.filter(
        productid=product
    ).order_by("position")
    images = [pa.assetid.preview for pa in product_assets]

    if product.featuredassetid and product.featuredassetid.preview not in images:
        images.insert(0, product.featuredassetid.preview)

    for variant in variants:
        if (
            variant.featuredassetid
            and variant.featuredassetid.preview not in images
        ):
            images.append(variant.featuredassetid.preview)

    if not images:
        images = [resolve_fallback_image(translation.slug)]

    prices = ProductVariantPrice.objects.filter(variantid__in=variants)
    price_values = [p.price / 100 for p in prices]

    min_price = min(price_values) if price_values else 0.0
    max_price = max(price_values) if price_values else 0.0

    detailed_variants = []
    for variant in variants:
        v_price_obj = prices.filter(variantid=variant).first()
        v_price = v_price_obj.price / 100 if v_price_obj else 0.0
        v_opts = ProductVariantOptionsProductOption.objects.filter(
            productvariantid=variant
        )
        v_opt_names = []
        for vo in v_opts:
            vo_trans = ProductOptionTranslation.objects.filter(
                baseid=vo.productoptionid, languagecode="en"
            ).first()
            if vo_trans:
                v_opt_names.append(vo_trans.name)
        v_image = (
            variant.featuredassetid.preview
            if variant.featuredassetid
            else images[0]
        )
        detailed_variants.append({
            "id": variant.id,
            "sku": variant.sku,
            "price": f"{v_price:.2f}",
            "options": ", ".join(v_opt_names),
            "image": v_image,
        })

    facet_links = ProductFacetValuesFacetValue.objects.filter(
        productid=product
    )
    facets = []
    for link in facet_links:
        f_trans = FacetValueTranslation.objects.filter(
            baseid=link.facetvalueid, languagecode="en"
        ).first()
        if f_trans:
            facets.append({
                "group": link.facetvalueid.facetid.code,
                "name": f_trans.name,
            })

    variant_options = ProductVariantOptionsProductOption.objects.filter(
        productvariantid__in=variants
    )
    unique_options_ids = variant_options.values_list(
        "productoptionid", flat=True
    ).distinct()
    unique_options = ProductOption.objects.filter(id__in=unique_options_ids)

    option_list = []
    for opt in unique_options:
        opt_trans = ProductOptionTranslation.objects.filter(
            baseid=opt, languagecode="en"
        ).first()
        if opt_trans:
            option_list.append({
                "group": opt.groupid.code,
                "name": opt_trans.name,
                "id": opt.id,
            })

    related_qs = (
        Product.objects.filter(enabled=True)
        .exclude(id=product.id)
        .order_by("?")[:4]
    )
    related_products = []
    for rp in related_qs:
        rt = ProductTranslation.objects.filter(
            baseid=rp, languagecode="en"
        ).first()
        if not rt:
            continue
        rv = ProductVariant.objects.filter(
            productid=rp, enabled=True
        ).first()
        if not rv:
            continue
        rp_price_obj = ProductVariantPrice.objects.filter(
            variantid=rv
        ).first()
        rp_price = rp_price_obj.price / 100 if rp_price_obj else 0.0
        rp_image = resolve_product_image(rv, rp, rt.slug)
        related_products.append({
            "name": rt.name,
            "price": f"{rp_price:.2f}",
            "image_url": rp_image,
            "slug": rt.slug,
        })

    if not related_products:
        related_products = get_mock_products()[:4]

    price_display = (
        f"{min_price:.2f}"
        if min_price == max_price
        else f"{min_price:.2f} - {max_price:.2f}"
    )

    context = {
        "product": product,
        "name": translation.name,
        "description": translation.description,
        "slug": translation.slug,
        "images": images,
        "main_image": images[0],
        "min_price": f"{min_price:.2f}",
        "max_price": f"{max_price:.2f}",
        "price_display": price_display,
        "facets": facets,
        "options": option_list,
        "detailed_variants": detailed_variants,
        "variants_count": variants.count(),
        "related_products": related_products,
    }

    return render(request, "landing/product.html", context)


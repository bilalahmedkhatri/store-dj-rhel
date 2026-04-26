# app/admin_dashboard.py
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta

from app.models import (
    Order, Product, Customer, Payment, Refund,
    StockLevel, ProductVariant, OrderLine,
    Promotion, Fulfillment, ProductTranslation, ProductVariantPrice,
    Collection, CollectionTranslation, CollectionProductVariantsProductVariant,
    Facet, FacetValue, Tag,
)


def _to_currency(minor_units):
    """Vendure stores all amounts × 100 (minor currency units)."""
    return (minor_units or 0) / 100


def dashboard_callback(request, context):
    now = timezone.now()
    today = now.date()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_30 = now - timedelta(days=30)
    last_7  = now - timedelta(days=7)

    # ─── Base querysets ───────────────────────────────────────────────────────
    placed_orders = Order.objects.filter(
        state__in=["PaymentAuthorized", "PaymentSettled", "Shipped", "Delivered"],
        orderplacedat__isnull=False,
    )

    # ─── KPI Summary Cards ────────────────────────────────────────────────────
    total_revenue_agg = placed_orders.aggregate(total=Sum("subtotalwithtax"))
    total_revenue = _to_currency(total_revenue_agg["total"])

    month_revenue_agg = placed_orders.filter(
        orderplacedat__gte=start_of_month
    ).aggregate(total=Sum("subtotalwithtax"))
    month_revenue = _to_currency(month_revenue_agg["total"])

    orders_total   = Order.objects.count()
    orders_today   = Order.objects.filter(createdat__date=today).count()
    orders_pending = Order.objects.filter(state="ArrangingPayment").count()
    orders_placed  = placed_orders.count()

    customers_total = Customer.objects.count()
    customers_month = Customer.objects.filter(createdat__gte=start_of_month).count()

    products_total   = Product.objects.count()
    products_enabled = Product.objects.filter(enabled=True).count()

    # ─── Inventory Alerts: low/out-of-stock variants ─────────────────────────
    low_stock = (
        StockLevel.objects
        .select_related("productvariantid", "stocklocationid")
        .filter(stockonhand__lte=5, stockonhand__gte=0)
        .order_by("stockonhand")[:10]
    )
    out_of_stock_count = StockLevel.objects.filter(stockonhand__lte=0).count()
    low_stock_count    = StockLevel.objects.filter(stockonhand__gt=0, stockonhand__lte=5).count()

    # ─── Payments & Refunds ───────────────────────────────────────────────────
    payments_settled = Payment.objects.filter(state="Settled")
    payments_error   = Payment.objects.filter(state="Error")
    total_collected  = _to_currency(payments_settled.aggregate(t=Sum("amount"))["t"])
    refunds_pending  = Refund.objects.filter(state="Pending").count()
    refunds_total    = _to_currency(Refund.objects.aggregate(t=Sum("total"))["t"])

    # ─── Active Promotions ────────────────────────────────────────────────────
    active_promos = (
        Promotion.objects
        .filter(enabled=True)
        .filter(
            Q(startsat__isnull=True) | Q(startsat__lte=now)
        )
        .filter(
            Q(endsat__isnull=True) | Q(endsat__gte=now)
        )
        .order_by("-priorityscore")[:5]
    )

    # ─── Top-selling product variants (by order line quantity) ────────────────
    top_variants = (
        OrderLine.objects
        .values("productvariantid")
        .annotate(
            total_qty=Sum("orderplacedquantity"),
            total_revenue=Sum("listprice"),
            order_count=Count("orderid", distinct=True),
        )
        .order_by("-total_qty")[:8]
    )

    # Enrich with SKU and translation name
    variant_ids = [v["productvariantid"] for v in top_variants]
    variants_map = {
        pv.id: pv
        for pv in ProductVariant.objects.filter(id__in=variant_ids)
    }
    translations_map = {
        t.baseid_id: t.name
        for t in ProductVariantTranslation_safe(variant_ids)
    }

    top_products = []
    for v in top_variants:
        vid = v["productvariantid"]
        pv  = variants_map.get(vid)
        top_products.append({
            "name": translations_map.get(vid) or (pv.sku if pv else f"SKU#{vid}"),
            "sku":  pv.sku if pv else "—",
            "qty":  v["total_qty"] or 0,
            "revenue": _to_currency(v["total_revenue"]),
            "orders": v["order_count"],
        })

    # ─── Recent Orders ────────────────────────────────────────────────────────
    recent_orders = (
        Order.objects
        .select_related("customerid")
        .filter(orderplacedat__isnull=False)
        .order_by("-orderplacedat")[:8]
    )

    # ─── Order State Breakdown ────────────────────────────────────────────────
    order_states = (
        Order.objects
        .values("state")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # ─── Fulfillment Overview ────────────────────────────────────────────────
    fulfillment_states = (
        Fulfillment.objects
        .values("state")
        .annotate(count=Count("id"))
        .order_by("-count")
    )

    # ─── Category / Collection Management ────────────────────────────────────
    collections_total   = Collection.objects.count()
    collections_root    = Collection.objects.filter(isroot=True).count()
    collections_private = Collection.objects.filter(isprivate=True).count()
    collections_public  = Collection.objects.filter(isprivate=False, isroot=False).count()

    # Top collections ranked by number of linked product variants
    top_collections_raw = (
        CollectionProductVariantsProductVariant.objects
        .values("collectionid")
        .annotate(variant_count=Count("productvariantid", distinct=True))
        .order_by("-variant_count")[:8]
    )

    # Resolve collection IDs → English names
    col_ids = [r["collectionid"] for r in top_collections_raw]
    col_trans = {
        t.baseid_id: t.name
        for t in CollectionTranslation.objects.filter(
            baseid_id__in=col_ids, languagecode="en"
        )
    }
    col_objects = {c.id: c for c in Collection.objects.filter(id__in=col_ids)}

    top_collections = []
    for r in top_collections_raw:
        cid = r["collectionid"]
        col = col_objects.get(cid)
        top_collections.append({
            "name": col_trans.get(cid) or f"Collection #{cid}",
            "variant_count": r["variant_count"],
            "isroot": col.isroot if col else False,
            "isprivate": col.isprivate if col else False,
            "id": cid,
        })

    # Recent collections (newest first)
    recent_collections = (
        Collection.objects
        .order_by("-createdat")[:5]
    )
    recent_collections_data = []
    for col in recent_collections:
        t = CollectionTranslation.objects.filter(baseid=col, languagecode="en").first()
        recent_collections_data.append({
            "id": col.id,
            "name": t.name if t else f"Collection #{col.id}",
            "isroot": col.isroot,
            "isprivate": col.isprivate,
            "created": col.createdat,
        })

    # ─── Facets & Tags ────────────────────────────────────────────────────────
    facets_total      = Facet.objects.count()
    facet_values_total = FacetValue.objects.count()

    try:
        tags_total = Tag.objects.count()
    except Exception:
        tags_total = 0

    context.update({
        # Summary KPIs
        "kpi": [
            {
                "title": "Total Revenue",
                "metric": f"Rs. {total_revenue:,.2f}",
                "sub": f"Rs. {month_revenue:,.2f} this month",
                "icon": "payments",
                "color": "green",
            },
            {
                "title": "Orders",
                "metric": f"{orders_total:,}",
                "sub": f"{orders_today} today · {orders_pending} pending",
                "icon": "shopping_cart",
                "color": "blue",
            },
            {
                "title": "Customers",
                "metric": f"{customers_total:,}",
                "sub": f"+{customers_month} this month",
                "icon": "group",
                "color": "purple",
            },
            {
                "title": "Products",
                "metric": f"{products_total:,}",
                "sub": f"{products_enabled} active · {products_total - products_enabled} disabled",
                "icon": "inventory_2",
                "color": "orange",
            },
        ],

        # Secondary stats row
        "stats": [
            {"label": "Settled Payments",  "value": f"Rs. {total_collected:,.2f}", "icon": "check_circle"},
            {"label": "Failed Payments",   "value": str(payments_error.count()),  "icon": "cancel",       "alert": payments_error.count() > 0},
            {"label": "Pending Refunds",   "value": str(refunds_pending),          "icon": "undo",         "alert": refunds_pending > 0},
            {"label": "Total Refunded",    "value": f"Rs. {refunds_total:,.2f}",      "icon": "currency_exchange"},
            {"label": "Out-of-Stock SKUs", "value": str(out_of_stock_count),       "icon": "warning",      "alert": out_of_stock_count > 0},
            {"label": "Low Stock SKUs",    "value": str(low_stock_count),          "icon": "inventory",    "alert": low_stock_count > 0},
        ],

        # Data sections
        "recent_orders":     recent_orders,
        "top_products":      top_products,
        "low_stock":         low_stock,
        "active_promos":     active_promos,
        "order_states":      order_states,
        "fulfillment_states": fulfillment_states,

        # Category management
        "category_stats": {
            "total":   collections_total,
            "root":    collections_root,
            "private": collections_private,
            "public":  collections_public,
        },
        "top_collections":    top_collections,
        "recent_collections": recent_collections_data,
        "facets_total":       facets_total,
        "facet_values_total": facet_values_total,
        "tags_total":         tags_total,

        # Quick links for admins
        "quick_links": [
            {"title": "Add Product",   "icon": "add_box",         "url": "/admin/app/product/add/"},
            {"title": "View Orders",   "icon": "shopping_cart",   "url": "/admin/app/order/"},
            {"title": "Customers",     "icon": "group",           "url": "/admin/app/customer/"},
            {"title": "Promotions",    "icon": "campaign",        "url": "/admin/app/promotion/"},
            {"title": "Stock Levels",  "icon": "inventory",       "url": "/admin/app/stocklevel/"},
            {"title": "Payments",      "icon": "payments",        "url": "/admin/app/payment/"},
            {"title": "Fulfillments",  "icon": "local_shipping",  "url": "/admin/app/fulfillment/"},
            {"title": "Settings",      "icon": "settings",        "url": "/admin/app/globalsettings/"},
        ],
    })
    return context


def ProductVariantTranslation_safe(variant_ids):
    """Return en translations for variant list, safely."""
    from app.models import ProductVariantTranslation
    if not variant_ids:
        return []
    return ProductVariantTranslation.objects.filter(
        baseid_id__in=variant_ids,
        languagecode="en",
    )

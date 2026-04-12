# app/admin_dashboard.py
from django.db.models import Sum
from app.models import Order, Product, Customer


def dashboard_callback(request, context):
    # Aggregate KPIs efficiently
    orders_qs = Order.objects.all()
    orders_count = orders_qs.count()

    revenue_agg = orders_qs.filter(
        state__in=["PaymentAuthorized", "PaymentSettled", "Shipped", "Delivered"]
    ).aggregate(total=Sum("totalwithtax"))
    revenue = (revenue_agg["total"] or 0) / 100  # Vendure stores amounts in minor units

    context.update({
        "kpi": [
            {
                "title": "Total Revenue",
                "metric": f"${revenue:,.2f}",
                "icon": "payments",
                "description": "Settled & authorized orders",
            },
            {
                "title": "Total Orders",
                "metric": f"{orders_count:,}",
                "icon": "shopping_cart",
                "description": "All time orders",
            },
            {
                "title": "Customers",
                "metric": f"{Customer.objects.count():,}",
                "icon": "group",
                "description": "Registered customers",
            },
            {
                "title": "Products",
                "metric": f"{Product.objects.count():,}",
                "icon": "inventory_2",
                "description": "Total products in catalog",
            },
        ],
        "recent_orders": Order.objects.select_related("customerid").order_by(
            "-orderplacedat"
        )[:10],
    })
    return context

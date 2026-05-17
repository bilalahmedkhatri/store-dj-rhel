from .register import register_view
from .products import products_view, product_detail_view
from .not_found import not_found_view
from .main import index, category_list, category_detail, all_products, serve_merchant_document
from .login import login_view, logout_view
from .cart import cart_view, add_to_cart_view, cart_update_view, cart_remove_view
from .checkout import checkout_view, payment_success_view, payment_failed_view, payment_pending_view, receipt_view
from .webhooks import gopayfast_webhook
from .dashboard import dashboard_view, add_address_view, profile_view
from .extra_pages import (
    faqs,
    about_us,
    contact_us,
    privacy_policy,
    terms_and_conditions,
    shipping_policy,
    return_policy,
    payment_methods,
    complaints,
    aml_policy,
    acceptable_use,
    merchant_agreement,
    pricing,
    kyc,
    refund_status,
    security,
    cookie_policy,
    status_page,
)

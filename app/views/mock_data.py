from __future__ import annotations


def get_mock_products() -> list[dict]:
    return [
        {
            "name": "Premium Wireless Headphones",
            "description": "Rich sound, clear mic, and all-day comfort.",
            "price": "299.99",
            "image_url": "/static/images/products/1.jpg",
            "slug": "premium-wireless-headphones",
            "variant_label": "Matte Black",
        },
        {
            "name": "Minimalist Smartwatch",
            "description": "Track fitness and notifications in style.",
            "price": "199.50",
            "image_url": "/static/images/products/2.jpg",
            "slug": "minimalist-smartwatch",
            "variant_label": "Silver",
        },
        {
            "name": "Urban Travel Backpack",
            "description": "Lightweight, durable, and laptop friendly.",
            "price": "89.00",
            "image_url": "/static/images/products/3.jpg",
            "slug": "urban-travel-backpack",
            "variant_label": "Graphite",
        },
        {
            "name": "Classic Leather Wallet",
            "description": "Slim profile with premium leather finish.",
            "price": "49.90",
            "image_url": "/static/images/products/4.jpg",
            "slug": "classic-leather-wallet",
            "variant_label": "Brown",
        },
        {
            "name": "Performance Running Shoes",
            "description": "Breathable comfort built for daily miles.",
            "price": "129.00",
            "image_url": "/static/images/products/5.jpg",
            "slug": "performance-running-shoes",
            "variant_label": "Blue / White",
        },
        {
            "name": "Essentials Hoodie",
            "description": "Soft fleece hoodie for everyday wear.",
            "price": "74.00",
            "image_url": "/static/images/products/6.jpg",
            "slug": "essentials-hoodie",
            "variant_label": "Charcoal",
        },
    ]


def get_mock_shop_filters() -> dict:
    return {
        "categories": ["Women", "Men", "Accessories", "Shoes", "Beauty"],
        "facet_groups": {
            "brand": ["MukhtaleefWear", "Urban Fit", "Nova Wear"],
            "material": ["Cotton", "Denim", "Leather", "Polyester"],
        },
        "option_groups": {
            "size": ["XS", "S", "M", "L", "XL"],
            "color": ["Black", "White", "Blue", "Red", "Beige"],
        },
        "price_min": 0.0,
        "price_max": 300.0,
    }


def get_mock_categories() -> list[dict]:
    return [
        {
            "id": None,
            "name": "Electronics",
            "slug": "electronics",
            "image_url": "/static/images/cat-image1.jpg",
            "url": "/products/",
        },
        {
            "id": None,
            "name": "Fashion",
            "slug": "fashion",
            "image_url": "/static/images/cat-image4.jpg",
            "url": "/products/",
        },
        {
            "id": None,
            "name": "Accessories",
            "slug": "accessories",
            "image_url": "/static/images/cat-image5.jpg",
            "url": "/products/",
        },
    ]


def get_mock_cart_context() -> dict:
    cart_items = [
        {
            "id": 1,
            "product": {
                "name": "Premium Wireless Headphones",
                "image": {"url": "/static/images/products/1.jpg"},
            },
            "variant": "Matte Black",
            "quantity": 1,
            "unit_price": 299.99,
            "total_price": 299.99,
        },
        {
            "id": 2,
            "product": {
                "name": "Minimalist Smartwatch",
                "image": {"url": "/static/images/products/2.jpg"},
            },
            "variant": "Silver",
            "quantity": 2,
            "unit_price": 199.50,
            "total_price": 399.00,
        },
    ]
    subtotal = sum(item["total_price"] for item in cart_items)
    shipping = 0.0 if subtotal >= 500 else 15.0
    tax = round(subtotal * 0.08, 2)
    total = round(subtotal + shipping + tax, 2)
    free_shipping_threshold = 500.0
    amount_to_free_shipping = max(0.0, free_shipping_threshold - subtotal)
    return {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "shipping": shipping,
        "tax": tax,
        "total": total,
        "amount_to_free_shipping": amount_to_free_shipping,
    }


def get_mock_contact_data() -> dict:
    return {
        "contact_heading": "Get in Touch",
        "contact_subheading": "We'd love to hear from you. Send us a message and we'll respond within 24 hours.",
        "contact_info": {
            "address_label": "Address",
            "address": "PLOT NO-LY-1518, NAYABAD, LYARI QUARTER,KARACHI, Karachi South Lyari Town",
            "phone_label": "Phone",
            "phone": "+92 331 42 44 144",
            "email_label": "Email",
            "email": "najeeb.back74@gmail.com",
        },
        "business_hours": [
            "Monday - Friday: 9:00 AM - 6:00 PM",
            "Saturday: 10:00 AM - 4:00 PM",
            "Sunday: Closed",
        ],
        "social_links": [
            {"icon": "fab fa-facebook-f", "url": "#"},
            {"icon": "fab fa-twitter", "url": "#"},
            {"icon": "fab fa-instagram", "url": "#"},
            {"icon": "fab fa-pinterest", "url": "#"},
        ],
    }


def get_mock_about_data() -> dict:
    return {
        "hero_title": "About MukhtaleefWear",
        "hero_subtitle": "Crafting quality products with passion and precision since 2025",
        "story_title": "Our Story",
        "story_paragraphs": [
            "Founded in 2025, MukhtaleefWear started with a simple mission: to bring high-quality, stylish products to customers who value both form and function.",
            "We believe that great design should be accessible to everyone. That is why we curate every product with a focus on durability, aesthetics, and affordability.",
            "Our team is dedicated to exceptional customer service and a seamless shopping experience.",
        ],
        "values": [
            {"title": "Quality First", "description": "We never compromise on materials or craftsmanship."},
            {"title": "Customer First", "description": "Your satisfaction is our top priority."},
            {"title": "Global Community", "description": "Serving customers across the world."},
        ],
        "team": [
            {"name": "Najeeb", "role": "Founder & CEO", "image": "images/team/najeed.jpeg"},
            {"name": "Abdul Qadeer", "role": "Lead Designer", "image": "images/team/abdul.jpeg"},
        ],
    }


def get_mock_privacy_policy_data() -> dict:
    return {
        "title": "Privacy Policy",
        "effective_date": "April 12, 2026",
        "sections": [
            {"title": "Information We Collect", "body": "We collect information you provide directly, including account and checkout details, in compliance with SBP Consumer Protection Directives."},
            {"title": "How We Use Your Information", "bullets": ["Process and fulfill orders", "Communicate about orders", "Improve our services", "Send promotions (opt-out available)", "Regulatory reporting to SBP/FMU"]},
            {"title": "PCI DSS & Data Security", "body": "We apply industry-standard PCI DSS v4.0 controls to protect your payment data. Sensitive card information is never stored on our servers."},
            {"title": "AML Record Retention", "body": "In accordance with AML/CFT Regulations, we retain customer identification and transaction records for a minimum of 10 years."},
            {"title": "Contact", "body": "For privacy questions or SBP CPD related queries, email privacy@MukhtaleefWear.com."},
        ],
    }


def get_mock_terms_data() -> dict:
    return {
        "title": "Terms of Service",
        "last_updated": "April 12, 2026",
        "sections": [
            {"title": "Acceptance of Terms", "body": "By using this website, you agree to these terms and the Electronic Transactions Ordinance (ETO), 2002 of Pakistan."},
            {"title": "Jurisdiction", "body": "These terms are governed by the laws of the Islamic Republic of Pakistan. Any disputes shall be subject to the exclusive jurisdiction of the courts in Karachi."},
            {"title": "Transaction Limits", "body": "Transactions are subject to limits defined by the State Bank of Pakistan (SBP) and your issuing bank."},
            {"title": "Liability Cap", "body": "Our liability for any transaction-related issue is capped at the total amount of the specific transaction in question."},
            {"title": "Orders and Payment", "body": "We may refuse or cancel orders when needed for fraud/security reasons as per AML/CFT guidelines."},
            {"title": "Contact", "body": "For legal questions, email legal@MukhtaleefWear.com."},
        ],
    }


def get_mock_refund_policy_data() -> dict:
    return {
        "title": "Returns & Refunds Policy",
        "last_updated": "April 12, 2026",
        "sections": [
            {"title": "7-Day Auto-Refund Guarantee", "body": "For failed transactions where amount is deducted, an auto-refund is initiated within 7 days as per SBP standards."},
            {"title": "Standard Returns", "body": "Most unused items can be returned within 30 days of delivery."},
            {"title": "Refund Processing Timeline", "body": "Once approved, refunds are typically processed within 10-12 business days depending on your bank's cycle."},
            {"title": "Dispute Escalation", "body": "If a refund is not received within the stated timeline, please contact our Compliance Officer or escalate to the Banking Mohtasib Pakistan (BMP)."},
            {"title": "Support", "body": "Need help? Contact returns@MukhtaleefWear.com."},
        ],
    }


def get_mock_shipping_policy_data() -> dict:
    return {
        "title": "Shipping Information",
        "subtitle": "Fast, reliable delivery worldwide",
        "shipping_rows": [
            {"method": "Standard Shipping", "time": "3-5 business days", "cost": "Rs. 199 (Free over Rs. 7000)"},
            {"method": "Express Shipping", "time": "1-2 business days", "cost": "Rs. 399"},
            {"method": "International Standard", "time": "7-14 business days", "cost": "Calculated at checkout"},
        ],
        "sections": [
            {"title": "Order Processing", "body": "Orders are processed within 1-2 business days."},
            {"title": "Tracking", "body": "Tracking details are shared by email once your order ships."},
            {"title": "Support", "body": "Shipping questions: shipping@MukhtaleefWear.com."},
        ],
    }


def get_mock_payment_methods_data() -> dict:
    return {
        "title": "Payment Methods",
        "subtitle": "Secure options at checkout",
        "methods": [
            {
                "name": "Cards & Wallets (Stripe)",
                "description": "Visa, Mastercard, American Express, and supported wallets are accepted.",
            },
            {
                "name": "Cash on Delivery (COD)",
                "description": "COD is available in selected regions and order ranges.",
            },
            {
                "name": "JazzCash",
                "description": "Pay through your JazzCash mobile account where available.",
            },
        ],
        "security_note": "Payments are encrypted in transit. For payment issues, contact support@MukhtaleefWear.com.",
    }

# Project Structure

This document provides a directory and file map of the project, excluding `.agent`, `.agents`, `.awesome-design`, `.sixth`, `dj_env`, `staticfiles`, and `dashboard` directories.

```text
.
├── .env
├── app/
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── forms.py
│   ├── migrations/
│   │   ├── 0001_initial.py
│   │   ├── 0002_address_administrator_asset_assetchannelschannel_and_more.py
│   │   └── __init__.py
│   ├── models.py
│   ├── services/
│   │   └── payfast_service.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   ├── views/
│   │   ├── cart.py
│   │   ├── cart_utils.py
│   │   ├── checkout.py
│   │   ├── extra_pages.py
│   │   ├── login.py
│   │   ├── main.py
│   │   ├── mock_data.py
│   │   ├── not_found.py
│   │   ├── products.py
│   │   ├── register.py
│   │   └── __init__.py
│   └── __init__.py
├── db.sqlite3
├── fix_models.py
├── gopayfast.md
├── manage.py
├── README.md
├── requirements.txt
├── seed.py
├── setup/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
├── static/
│   ├── css/
│   │   ├── cart-toast.css
│   │   ├── custom.css
│   │   ├── form-styles.css
│   │   ├── product-page.css
│   │   ├── styles.css
│   │   └── tailwind.css
│   ├── images/
│   │   ├── brands/
│   │   │   ├── html.svg
│   │   │   ├── js.svg
│   │   │   ├── laravel.svg
│   │   │   ├── php.svg
│   │   │   ├── react.svg
│   │   │   ├── tailwind.svg
│   │   │   └── typescript.svg
│   │   ├── main-slider/
│   │   │   ├── 2.png
│   │   │   ├── 4.jpg
│   │   │   └── 5.jpg
│   │   ├── products/
│   │   │   ├── 1.jpg
│   │   │   ├── 2.jpg
│   │   │   ├── 3.jpg
│   │   │   ├── 4.jpg
│   │   │   ├── 5.jpg
│   │   │   ├── 6.jpg
│   │   │   ├── 7.jpg
│   │   │   ├── 8.jpg
│   │   │   └── product.jpg
│   │   ├── single-product/
│   │   │   ├── 1.jpg
│   │   │   ├── 2.jpg
│   │   │   ├── 3.jpg
│   │   │   ├── 4.jpg
│   │   │   └── 5.jpg
│   │   ├── social_icons/
│   │   │   ├── facebook.svg
│   │   │   ├── instagram.svg
│   │   │   ├── paypal.svg
│   │   │   ├── pinterest.svg
│   │   │   ├── stripe.svg
│   │   │   ├── twitter.svg
│   │   │   ├── viber.svg
│   │   │   ├── visa.svg
│   │   │   └── youtube.svg
│   │   ├── 404.jpg
│   │   ├── banner1.jpg
│   │   ├── cart-shopping.svg
│   │   ├── cat-image1.jpg
│   │   ├── cat-image4.jpg
│   │   ├── cat-image5.jpg
│   │   ├── customer-stories.jpg
│   │   ├── fashion-trends.jpg
│   │   ├── filter-down-arrow.svg
│   │   ├── filter-up-arrow.svg
│   │   ├── search-icon.svg
│   │   ├── stylisng-tips.jpg
│   │   ├── template-logo.png
│   │   └── template-white-logo.png
│   ├── js/
│   │   ├── cart-handler.js
│   │   ├── cart-page.js
│   │   ├── checkout.js
│   │   ├── faq.js
│   │   ├── product-page.js
│   │   └── script.js
├── templates/
│   ├── components/
│   │   ├── banners.html
│   │   ├── blog_section.html
│   │   ├── brands.html
│   │   ├── category_detail.html
│   │   ├── cta_banner.html
│   │   ├── latest_products.html
│   │   ├── popular_products.html
│   │   ├── products_filters.html
│   │   ├── slider.html
│   │   ├── storefront_feature_cards.html
│   │   ├── storefront_hero_strip.html
│   │   ├── storefront_icon_row.html
│   │   ├── storefront_product_wall.html
│   │   ├── storefront_view_more.html
│   │   └── subscribe.html
│   ├── emails/
│   │   └── order_confirmation.html
│   └── landing/
│       ├── about.html
│       ├── all_products.html
│       ├── base.html
│       ├── body.html
│       ├── cart.html
│       ├── category_detail.html
│       ├── checkout.html
│       ├── contact.html
│       ├── error.html
│       ├── faq.html
│       ├── footer.html
│       ├── header.html
│       ├── login.html
│       ├── meta.html
│       ├── not_found.html
│       ├── payment_methods.html
│       ├── privacy.html
│       ├── product.html
│       ├── products.html
│       ├── register.html
│       ├── return.html
│       ├── shipping.html
│       └── terms.html
└── tmp/
    ├── check_options.py
    ├── check_products.py
    ├── check_variants.py
    ├── seed_products.py
    └── seed_variants.py
```

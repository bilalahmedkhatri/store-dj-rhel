# Store DJ Reheel

Django storefront project with landing pages, product/category views, and static UI components.

## Quick Start

1. Create `.env` with database credentials used by `setup/settings.py`.
2. Activate virtual env:
   - Windows PowerShell: `.\dj_env\Scripts\Activate.ps1`
3. Run checks and start:
   - `python manage.py check`
   - `python manage.py runserver`

## Seed / Demo Data

- Category and product seed script:
  - `python seed.py`
  - `python seed.py --reset`

This project also includes UI mock fallback data in `app/views/mock_data.py` for landing and policy/contact pages.

## Recent UI Notes

- Home body uses componentized sections under `templates/components/`.
- Product grid supports a **View More** interaction:
  - button in `templates/components/storefront_view_more.html`
  - cards in `templates/components/storefront_product_wall.html`
  - behavior in `static/js/script.js`
- Footer is redesigned to a multi-column marketplace style in `templates/landing/footer.html`.

## Main Paths

- Django settings: `setup/settings.py`
- App views: `app/views/`
- Templates: `templates/landing/`, `templates/components/`
- Static assets: `static/`

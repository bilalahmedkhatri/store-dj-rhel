# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django 6.0.3 e-commerce storefront application with a focus on Pakistani market compliance, particularly for GoPayFast payment integration. The project follows a Vendure-inspired data model with collections (categories), products, variants, and complex relationships.

Key features include:
- Product catalog with categories and search
- Shopping cart functionality with session storage
- Payment processing through PayFast/GoPayFast
- Merchant onboarding and document management
- SBP (State Bank of Pakistan) compliance pages
- Responsive UI with Tailwind CSS

## Architecture Overview

### Core Components

1. **Models Layer (`app/models.py`)**
   - Auto-generated from existing database schema
   - Vendure-style e-commerce entities: Products, Collections, Variants, Assets
   - Merchant profiles with document storage (CNIC, utility bills)
   - Complex relationships through join tables (CollectionProductVariantsProductVariant, etc.)

2. **Views Layer (`app/views/`)**
   - Main storefront pages (home, categories, products)
   - Authentication (login, register)
   - Cart management (add, update, remove)
   - Checkout and payment flows
   - Extra pages (FAQ, About, Contact, policies)
   - Webhook handlers for payment callbacks

3. **Services Layer (`app/services/`)**
   - PayFast integration service with signature verification
   - Safepay alternative payment processor

4. **Templates (`templates/`)**
   - Landing pages for storefront
   - Component-based UI structure
   - Email templates

5. **Static Assets (`static/`)**
   - CSS (Tailwind + custom styles)
   - JavaScript for interactivity
   - Image assets

### Key Patterns

- Session-based shopping cart stored in `request.session['store_cart']`
- Mock data fallback system for development
- Multi-language support (primarily English)
- Security-focused with HMAC signature verification for webhooks
- PCI-DSS and SBP compliance considerations

## Common Development Tasks

### Running the Application

```bash
# Activate virtual environment
.\dj_env\Scripts\Activate.ps1  # Windows PowerShell

# Run development server
python manage.py runserver

# Run database checks
python manage.py check
```

### Working with Database

```bash
# Make migrations (if changing models)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Seed demo data
python seed.py
python seed.py --reset  # Reset and reseed
```

### Testing Payment Integration

The project includes both PayFast and Safepay integration:
- PayFast configuration in `app/services/payfast_service.py`
- Webhook handler in `app/views/webhooks.py`
- Environment variables for merchant credentials

## Code Navigation Tips

### Finding Specific Components

- **Product Views**: `app/views/main.py` (index, category browsing)
- **Cart System**: `app/views/cart.py` and `app/views/cart_utils.py`
- **Checkout Flow**: `app/views/checkout.py`
- **Payment Integration**: `app/services/payfast_service.py`
- **Webhooks**: `app/views/webhooks.py`
- **Merchant Features**: Various views with staff/admin decorators
- **Policy Pages**: `app/views/extra_pages.py`

### Understanding Data Models

The models are complex due to Vendure inspiration:
- Collections = Categories (with hierarchy via CollectionClosure)
- Products have multiple Variants
- Assets store media references
- Prices stored in separate ProductVariantPrice table
- Relationships managed through join tables

### Template Structure

- Base template: `templates/landing/base.html`
- Component templates: `templates/components/`
- Landing page sections: `templates/landing/body.html`
- Individual page templates in `templates/landing/`

## Important Considerations

### SBP Compliance

This project requires State Bank of Pakistan compliance pages as documented in `gopayfast.md`. Many legal pages are still pending implementation:
- Merchant Agreement
- AML/KYC Policy
- Acceptable Use Policy
- Cookie Policy
- Refund Status Lookup
- Complaints/Grievance Form

### Security Aspects

- Webhook signature verification with HMAC-SHA256
- Staff-only access for merchant documents
- CSRF protection on forms
- Session management for carts

### Performance Considerations

- Database queries optimized with `select_related` and `prefetch_related`
- Mock data fallback for when database is empty
- Lazy loading for images (in templates)

## Environment Variables

Required environment variables (in `.env` file):
- `DJANGO_SECRET_KEY`: Django secret key
- `PAYFAST_MERCHANT_ID`: GoPayFast merchant identifier
- `PAYFAST_SECURED_KEY`: GoPayFast security key
- Database credentials for PostgreSQL (optional, falls back to SQLite)

## Testing

Unit tests are located in `app/tests.py`. Run with:

```bash
python manage.py test
```

Frontend functionality can be tested by:
1. Running the development server
2. Navigating through pages
3. Adding items to cart
4. Testing checkout flow (currently simulated)
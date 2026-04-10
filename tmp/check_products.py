
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from app.models import Product, ProductTranslation, ProductVariant, ProductVariantPrice

try:
    product_count = Product.objects.count()
    print(f"Product count: {product_count}")
except Exception as e:
    print(f"Error querying Product: {e}")

import os
import django
import sys

# Add current directory to sys.path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from app.models import Product, ProductVariant, ProductTranslation

def check_products():
    products = Product.objects.all()
    print(f"Total products: {products.count()}")
    
    for p in products:
        trans = ProductTranslation.objects.filter(baseid=p, languagecode='en').first()
        name = trans.name if trans else f"Unknown (ID: {p.id})"
        variants = ProductVariant.objects.filter(productid=p)
        print(f"Product: {name} (ID: {p.id}) - Variants: {variants.count()}")
        if variants.count() == 0:
            print(f"  -> NO VARIANTS FOUND")

if __name__ == "__main__":
    check_products()

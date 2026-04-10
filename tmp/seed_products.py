
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from app.models import Product, ProductTranslation, ProductVariant, ProductVariantPrice, Asset

def seed():
    # Create an asset
    asset = Asset.objects.create(
        createdat=timezone.now(),
        updatedat=timezone.now(),
        name="Dummy Product Image",
        type="IMAGE",
        mimetype="image/jpeg",
        width=400,
        height=400,
        filesize=1000,
        source="https://picsum.photos/400/400",
        preview="https://picsum.photos/400/400"
    )

    products_data = [
        {"name": "Elegant Watch", "price": 12000, "description": "A very elegant watch for special occasions."},
        {"name": "Modern Camera", "price": 45000, "description": "Capture your best moments with high precision."},
        {"name": "Leather Wallet", "price": 3500, "description": "High-quality leather wallet for daily use."},
        {"name": "Wireless Headphones", "price": 8500, "description": "Experience sound like never before."},
    ]

    for data in products_data:
        product = Product.objects.create(
            createdat=timezone.now(),
            updatedat=timezone.now(),
            enabled=True,
            featuredassetid=asset
        )
        
        ProductTranslation.objects.create(
            createdat=timezone.now(),
            updatedat=timezone.now(),
            languagecode="en",
            name=data["name"],
            slug=data["name"].lower().replace(" ", "-"),
            description=data["description"],
            baseid=product
        )
        
        variant = ProductVariant.objects.create(
            createdat=timezone.now(),
            updatedat=timezone.now(),
            enabled=True,
            sku=f"SKU-{product.id}",
            outofstockthreshold=0,
            useglobaloutofstockthreshold=True,
            trackinventory="NONE",
            productid=product
        )
        
        ProductVariantPrice.objects.create(
            createdat=timezone.now(),
            updatedat=timezone.now(),
            currencycode="USD",
            price=data["price"],
            variantid=variant
        )

    print("Seeding completed successfully!")

if __name__ == "__main__":
    seed()

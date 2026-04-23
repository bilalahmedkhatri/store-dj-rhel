import os
import django
import sys
import uuid
from django.utils import timezone

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from app.models import (
    Product, ProductTranslation, ProductVariant, ProductVariantPrice, Asset, 
    ProductOptionGroup, ProductOption, ProductOptionGroupTranslation, 
    ProductOptionTranslation, ProductVariantOptionsProductOption,
    ProductAsset, ProductVariantTranslation
)

def seed_loewe():
    now = timezone.now()
    
    # 1. Create Assets (Gallery)
    images = [
        ('loewe-1.jpg', 'Loewe Set Front'),
        ('loewe-2.jpg', 'Loewe Set Side'),
        ('loewe-3.jpg', 'Loewe Set Detail'),
        ('loewe-4.jpg', 'Loewe Set Lifestyle'),
    ]
    
    asset_objs = []
    for img_name, title in images:
        path = f'/static/images/products/{img_name}'
        asset = Asset.objects.create(
            createdat=now, updatedat=now, name=title, type='IMAGE', 
            mimetype='image/jpeg', width=800, height=1000, filesize=100000,
            source=path, preview=path
        )
        asset_objs.append(asset)

    # 2. Create Product
    product = Product.objects.create(
        createdat=now, updatedat=now, enabled=True, featuredassetid=asset_objs[0]
    )
    
    ProductTranslation.objects.create(
        createdat=now, updatedat=now, languagecode='en', 
        name='Loewe Inspired Taupe Co-ord Set',
        slug='loewe-inspired-taupe-coord-set',
        description='Premium polyester-viscose blend two-piece set. Features utility pockets, matte gabardine finish, and matching trousers for a modern minimalist look.',
        baseid=product
    )
    
    # 3. Link Assets to Product (Gallery)
    for i, asset in enumerate(asset_objs):
        ProductAsset.objects.create(
            createdat=now, updatedat=now, assetid=asset, productid=product, position=i
        )

    # 4. Create Option Group: Size
    size_group = ProductOptionGroup.objects.create(
        createdat=now, updatedat=now, code='size', productid=product
    )
    ProductOptionGroupTranslation.objects.create(
        createdat=now, updatedat=now, languagecode='en', name='Size', baseid=size_group
    )
    
    sizes = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')]
    
    for code, label in sizes:
        # Create Option
        opt = ProductOption.objects.create(
            createdat=now, updatedat=now, code=code, groupid=size_group
        )
        ProductOptionTranslation.objects.create(
            createdat=now, updatedat=now, languagecode='en', name=label, baseid=opt
        )
        
        # Create Variant
        variant = ProductVariant.objects.create(
            createdat=now, updatedat=now, enabled=True, 
            sku=f'LOEWE-TAUPE-{code}',
            outofstockthreshold=5, useglobaloutofstockthreshold=True, 
            trackinventory='TRUE', productid=product, featuredassetid=asset_objs[0]
        )
        
        # Variant Translation
        ProductVariantTranslation.objects.create(
            createdat=now, updatedat=now, languagecode='en', 
            name=f'Loewe Inspired Set - {label}', baseid=variant
        )
        
        # Variant Price (12,500 PKR)
        ProductVariantPrice.objects.create(
            createdat=now, updatedat=now, currencycode='PKR', price=1250000, variantid=variant
        )
        
        # Link Variant to Option
        ProductVariantOptionsProductOption.objects.create(
            productvariantid=variant, productoptionid=opt
        )
    
    print("Successfully seeded Loewe Inspired Co-ord Set with 4 images and 4 size variants.")

if __name__ == "__main__":
    seed_loewe()

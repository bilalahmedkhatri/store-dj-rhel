import os
import django
import sys
from django.utils import timezone

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from app.models import (
    Product, ProductVariant, ProductVariantPrice, Asset, 
    ProductOptionGroup, ProductOption, ProductOptionGroupTranslation, 
    ProductOptionTranslation, ProductVariantOptionsProductOption
)

def seed_variants():
    now = timezone.now()
    
    # 1. Elegant Watch (ID: 1)
    watch = Product.objects.get(id=1)
    
    # Create Option Group: Material
    material_group = ProductOptionGroup.objects.create(
        createdat=now, updatedat=now, code='material', productid=watch
    )
    ProductOptionGroupTranslation.objects.create(
        createdat=now, updatedat=now, languagecode='en', name='Material', baseid=material_group
    )
    
    # Create Options: Silver, Gold
    silver_opt = ProductOption.objects.create(
        createdat=now, updatedat=now, code='silver', groupid=material_group
    )
    ProductOptionTranslation.objects.create(
        createdat=now, updatedat=now, languagecode='en', name='Silver', baseid=silver_opt
    )
    
    gold_opt = ProductOption.objects.create(
        createdat=now, updatedat=now, code='gold', groupid=material_group
    )
    ProductOptionTranslation.objects.create(
        createdat=now, updatedat=now, languagecode='en', name='Gold', baseid=gold_opt
    )
    
    # Create Assets (Images)
    asset_silver = Asset.objects.create(
        createdat=now, updatedat=now, name='Watch Silver', type='IMAGE', 
        mimetype='image/jpeg', width=800, height=600, filesize=50000,
        source='static/images/products/1.jpg', preview='static/images/products/1.jpg'
    )
    asset_gold = Asset.objects.create(
        createdat=now, updatedat=now, name='Watch Gold', type='IMAGE', 
        mimetype='image/jpeg', width=800, height=600, filesize=60000,
        source='static/images/products/5.jpg', preview='static/images/products/5.jpg'
    )
    
    # Create Variants
    # Delete existing variants for watch to avoid confusion if any
    ProductVariant.objects.filter(productid=watch).delete()
    
    v_silver = ProductVariant.objects.create(
        createdat=now, updatedat=now, enabled=True, sku='WATCH-SILVER',
        outofstockthreshold=0, useglobaloutofstockthreshold=True, 
        trackinventory='FALSE', productid=watch, featuredassetid=asset_silver
    )
    ProductVariantPrice.objects.create(
        createdat=now, updatedat=now, currencycode='USD', price=15000, variantid=v_silver
    )
    ProductVariantOptionsProductOption.objects.create(
        productvariantid=v_silver, productoptionid=silver_opt
    )
    
    v_gold = ProductVariant.objects.create(
        createdat=now, updatedat=now, enabled=True, sku='WATCH-GOLD',
        outofstockthreshold=0, useglobaloutofstockthreshold=True, 
        trackinventory='FALSE', productid=watch, featuredassetid=asset_gold
    )
    ProductVariantPrice.objects.create(
        createdat=now, updatedat=now, currencycode='USD', price=25000, variantid=v_gold
    )
    ProductVariantOptionsProductOption.objects.create(
        productvariantid=v_gold, productoptionid=gold_opt
    )
    
    print("Seeded variants for Elegant Watch.")

    # 2. Wireless Headphones (ID: 4)
    headphones = Product.objects.get(id=4)
    
    # Create Option Group: Color
    color_group = ProductOptionGroup.objects.create(
        createdat=now, updatedat=now, code='color', productid=headphones
    )
    ProductOptionGroupTranslation.objects.create(
        createdat=now, updatedat=now, languagecode='en', name='Color', baseid=color_group
    )
    
    # Create Options: Black, White
    black_opt = ProductOption.objects.create(
        createdat=now, updatedat=now, code='black', groupid=color_group
    )
    ProductOptionTranslation.objects.create(
        createdat=now, updatedat=now, languagecode='en', name='Black', baseid=black_opt
    )
    
    white_opt = ProductOption.objects.create(
        createdat=now, updatedat=now, code='white', groupid=color_group
    )
    ProductOptionTranslation.objects.create(
        createdat=now, updatedat=now, languagecode='en', name='White', baseid=white_opt
    )
    
    # Create Assets
    asset_black = Asset.objects.create(
        createdat=now, updatedat=now, name='Headphones Black', type='IMAGE', 
        mimetype='image/jpeg', width=800, height=600, filesize=70000,
        source='static/images/products/4.jpg', preview='static/images/products/4.jpg'
    )
    asset_white = Asset.objects.create(
        createdat=now, updatedat=now, name='Headphones White', type='IMAGE', 
        mimetype='image/jpeg', width=800, height=600, filesize=40000,
        source='static/images/products/8.jpg', preview='static/images/products/8.jpg'
    )
    
    # Create Variants
    ProductVariant.objects.filter(productid=headphones).delete()
    
    v_black = ProductVariant.objects.create(
        createdat=now, updatedat=now, enabled=True, sku='HP-BLACK',
        outofstockthreshold=0, useglobaloutofstockthreshold=True, 
        trackinventory='FALSE', productid=headphones, featuredassetid=asset_black
    )
    ProductVariantPrice.objects.create(
        createdat=now, updatedat=now, currencycode='USD', price=8900, variantid=v_black
    )
    ProductVariantOptionsProductOption.objects.create(
        productvariantid=v_black, productoptionid=black_opt
    )
    
    v_white = ProductVariant.objects.create(
        createdat=now, updatedat=now, enabled=True, sku='HP-WHITE',
        outofstockthreshold=0, useglobaloutofstockthreshold=True, 
        trackinventory='FALSE', productid=headphones, featuredassetid=asset_white
    )
    ProductVariantPrice.objects.create(
        createdat=now, updatedat=now, currencycode='USD', price=9500, variantid=v_white
    )
    ProductVariantOptionsProductOption.objects.create(
        productvariantid=v_white, productoptionid=white_opt
    )
    
    print("Seeded variants for Wireless Headphones.")

if __name__ == "__main__":
    seed_variants()

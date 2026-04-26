import os
import django
import random
import glob
import sys
import cloudinary.uploader
from django.utils import timezone

# 1. Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
try:
    django.setup()
    # Explicitly configure cloudinary from settings
    from django.conf import settings
    import cloudinary
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
        api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
        api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
        secure=True
    )
except Exception as e:
    print(f"Error setting up Django: {e}")
    sys.exit(1)

from app.models import Asset, Product, ProductVariant, ProductVariantPrice

def run_comprehensive_update():
    # 2. Get all images from 'Image sits'
    image_dir = 'Image sits'
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp']
    local_images = []
    for ext in extensions:
        local_images.extend(glob.glob(os.path.join(image_dir, ext)))
    
    if not local_images:
        print(f"No images found in {image_dir}")
        return

    print(f"Found {len(local_images)} local images. Starting Cloudinary migration...")

    # 3. Upload ALL images and create new Asset records
    new_assets = []
    for i, local_path in enumerate(local_images):
        filename = os.path.basename(local_path)
        print(f"[{i+1}/{len(local_images)}] Uploading {filename}...")
        
        try:
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                local_path,
                folder="assets/",
                public_id=f"prod_{os.path.splitext(filename)[0]}_{random.getrandbits(16)}",
                overwrite=True,
                resource_type="image"
            )
            
            cloud_url = upload_result.get('secure_url')
            
            # Create fresh Asset record
            asset = Asset.objects.create(
                createdat=timezone.now(),
                updatedat=timezone.now(),
                name=filename,
                type='IMAGE',
                mimetype=upload_result.get('format', 'image/jpeg'),
                filesize=upload_result.get('bytes', 0),
                width=upload_result.get('width', 0),
                height=upload_result.get('height', 0),
                source=cloud_url,
                preview=cloud_url
            )
            new_assets.append(asset)
            print(f"   Created Asset ID: {asset.id} -> {cloud_url}")
            
        except Exception as e:
            print(f"   Failed {filename}: {e}")

    if not new_assets:
        print("No assets were created. Aborting product update.")
        return

    # 4. Randomly link NEW assets to existing Products and Variants
    print("\nLinking new assets to products and variants...")
    
    products = Product.objects.all()
    for p in products:
        p.featuredassetid = random.choice(new_assets)
        p.save()
    
    variants = ProductVariant.objects.all()
    for v in variants:
        v.featuredassetid = random.choice(new_assets)
        v.save()
    
    print(f"Updated {products.count()} products and {variants.count()} variants with cloud assets.")

    # 5. Update Product Prices with random values (2000-3000)
    print("\nRandomizing prices (2000-3000 PKR)...")
    prices = ProductVariantPrice.objects.all()
    p_count = 0
    for p in prices:
        # Check scale (standard vs cents)
        if p.price >= 100000: # Cents scale
            p.price = random.randrange(200000, 310000, 10000)
        else: # Standard scale
            p.price = random.randrange(2000, 3100, 100)
        p.save()
        p_count += 1
    
    print(f"Updated {p_count} price records.")
    print("\nMigration to Cloudinary and Price Update Complete!")

if __name__ == "__main__":
    run_comprehensive_update()

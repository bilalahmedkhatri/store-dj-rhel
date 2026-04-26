import os
import django
import random
import glob
import sys

# 1. Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
try:
    django.setup()
except Exception as e:
    print(f"Error setting up Django: {e}")
    print("Make sure you have installed 'django-cloudinary-storage' and 'cloudinary' inside your venv.")
    sys.exit(1)

from app.models import Asset, ProductVariantPrice
import cloudinary.uploader

def run_update():
    # 2. Get all images from 'Image sits'
    image_dir = 'Image sits'
    extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp']
    local_images = []
    for ext in extensions:
        local_images.extend(glob.glob(os.path.join(image_dir, ext)))
    
    if not local_images:
        print(f"No images found in {image_dir}")
        return

    print(f"Found {len(local_images)} local images.")

    # 3. Update Assets with random Cloudinary uploads
    assets = Asset.objects.all()
    print(f"Found {assets.count()} assets in database to update.")

    for i, asset in enumerate(assets):
        # Pick a random image
        local_path = random.choice(local_images)
        filename = os.path.basename(local_path)
        
        print(f"[{i+1}/{len(assets)}] Uploading {filename} for Asset: {asset.name or asset.id}...")
        
        try:
            # Upload to Cloudinary
            upload_result = cloudinary.uploader.upload(
                local_path,
                folder="assets/",
                public_id=f"auto_{os.path.splitext(filename)[0]}_{random.getrandbits(32)}",
                overwrite=True,
                resource_type="image"
            )
            
            # Get Cloud URL
            cloud_url = upload_result.get('secure_url')
            
            # Update Asset fields
            asset.source = cloud_url
            asset.preview = cloud_url
            asset.name = filename
            asset.mimetype = upload_result.get('format', 'image/jpeg')
            asset.filesize = upload_result.get('bytes', 0)
            asset.width = upload_result.get('width', 0)
            asset.height = upload_result.get('height', 0)
            asset.type = 'IMAGE'
            
            # Save will trigger pre_save, but we already have metadata from Cloudinary
            asset.save()
            print(f"   Success: {cloud_url}")
            
        except Exception as e:
            print(f"   Failed to upload {filename}: {e}")

    # 4. Update Product Prices
    print("\nUpdating product prices with random values (2000-3000, increments of 100)...")
    
    # 4.1 Update Standard Scale (2000 -> Random)
    prices_std = ProductVariantPrice.objects.all()
    count1 = 0
    for p in prices_std:
        # Random price in [2000, 2100, ..., 3000]
        p.price = random.randrange(2000, 3100, 100)
        p.save()
        count1 += 1

    print(f"Updated {count1} records with random prices.")

    print("\nAll tasks completed successfully!")

if __name__ == "__main__":
    run_update()

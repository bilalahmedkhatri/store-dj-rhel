import os
import django
import random
import sys
import cloudinary.uploader
from django.utils import timezone

# 1. Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
try:
    django.setup()
    from django.conf import settings
    import cloudinary
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
        api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
        api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
        secure=True
    )
except Exception as e:
    print(f"Error setting up Django/Cloudinary: {e}")
    sys.exit(1)

from app.models import Asset, Collection, CollectionTranslation

def seed_category_images():
    # 2. Define High-End Fashion URLs for Categories
    # These are curated from Unsplash fashion collections
    category_visuals = {
        "seed-premium": "https://images.unsplash.com/photo-1490481651871-ab68de25d43d?q=80&w=1200",
        "seed-footwear": "https://images.unsplash.com/photo-1549298916-b41d501d3772?q=80&w=1200",
        "seed-accessories": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=1200",
        "seed-summer": "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?q=80&w=1200",
        "seed-new-arrivals": "https://images.unsplash.com/photo-1445205170230-053b83016050?q=80&w=1200",
        "seed-fashion": "https://images.unsplash.com/photo-1483985988355-763728e1935b?q=80&w=1200",
        "seed-electronics": "https://images.unsplash.com/photo-1519389950473-47ba0277781c?q=80&w=1200",
        "seed-men-eastern": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?q=80&w=1200", # Stylized placeholder
        "seed-men-western": "https://images.unsplash.com/photo-1617127365659-c47fa864d8bc?q=80&w=1200",
    }

    print(f"Starting Category Image Seeding via Cloudinary...")

    for slug, url in category_visuals.items():
        # Check if collection exists
        trans = CollectionTranslation.objects.filter(slug=slug, languagecode='en').first()
        if not trans or not trans.baseid:
            print(f"   Skipping {slug}: Collection not found in DB.")
            continue

        collection = trans.baseid
        print(f"Processing '{trans.name}'...")

        try:
            # 1. Upload Remote URL directly to Cloudinary
            upload_result = cloudinary.uploader.upload(
                url,
                folder="categories/",
                public_id=f"cat_{slug}",
                overwrite=True,
                resource_type="image"
            )
            
            cloud_url = upload_result.get('secure_url')

            # 2. Create Asset Record
            asset = Asset.objects.create(
                createdat=timezone.now(),
                updatedat=timezone.now(),
                name=f"Cover for {trans.name}",
                type='IMAGE',
                mimetype='image/jpeg',
                filesize=upload_result.get('bytes', 0),
                width=upload_result.get('width', 0),
                height=upload_result.get('height', 0),
                source=cloud_url,
                preview=cloud_url
            )

            # 3. Link Asset to Collection
            collection.featuredassetid = asset
            collection.save()
            
            print(f"   Success: Assigned cloud image to {trans.name}")

        except Exception as e:
            print(f"   Failed to process {slug}: {e}")

    print("\nCategory image migration complete!")

if __name__ == "__main__":
    seed_category_images()

import os
import django
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
    # Curated High-End Men's Fashion Visuals
    category_visuals = {
        "seed-suits": "https://images.unsplash.com/photo-1594932224828-b4b059b6f6ee?q=80&w=1200",
        "seed-formal-shirts": "https://images.unsplash.com/photo-1621072156002-e2fcced0b170?q=80&w=1200",
        "seed-casual-shirts": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?q=80&w=1200",
        "seed-tshirts": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?q=80&w=1200",
        "seed-hoodies": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?q=80&w=1200",
        "seed-outerwear": "https://images.unsplash.com/photo-1551028719-00167b16eac5?q=80&w=1200",
        "seed-eastern": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?q=80&w=1200",
        "seed-denim": "https://images.unsplash.com/photo-1542272604-787c3835535d?q=80&w=1200",
        "seed-chinos": "https://images.unsplash.com/photo-1624371414361-e6e8eaad858e?q=80&w=1200",
        "seed-trousers": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?q=80&w=1200",
        "seed-shorts": "https://images.unsplash.com/photo-1591195853828-11db59a44f6b?q=80&w=1200",
        "seed-activewear": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?q=80&w=1200",
        "seed-innerwear": "https://images.unsplash.com/photo-1582738411706-bfc8e691d1c2?q=80&w=1200",
        "seed-accessories": "https://images.unsplash.com/photo-1627123424574-724758594e93?q=80&w=1200",
    }

    print(f"Starting Men's Fashion Category Image Seeding via Cloudinary...")

    for slug, url in category_visuals.items():
        trans = CollectionTranslation.objects.filter(slug=slug, languagecode='en').first()
        if not trans or not trans.baseid:
            print(f"   Skipping {slug}: Collection not found.")
            continue

        collection = trans.baseid
        print(f"Processing '{trans.name}'...")

        try:
            upload_result = cloudinary.uploader.upload(
                url,
                folder="categories/",
                public_id=f"cat_{slug}",
                overwrite=True,
                resource_type="image"
            )
            
            cloud_url = upload_result.get('secure_url')

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

            collection.featuredassetid = asset
            collection.save()
            
            print(f"   Success: Assigned cloud image to {trans.name}")

        except Exception as e:
            print(f"   Failed to process {slug}: {e}")

    print("\nCategory image migration complete!")

if __name__ == "__main__":
    seed_category_images()

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
    print(f"Error: {e}. Please ensure venv is active and packages installed.")
    sys.exit(1)

from app.models import Asset, Collection, CollectionTranslation

def fix_missing_images():
    # Targeted URLs for the missing categories
    fix_data = {
        # "seed-shop-root": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?q=80&w=1200", 
        # "seed-suits": "https://images.unsplash.com/photo-1594932224828-b4b059b6f6ee?q=80&w=1200",      
        "seed-formal-shirts": "https://images.unsplash.com/photo-1621072156002-e2fcced0b170?q=80&w=1200", 
        # "seed-chinos": "https://images.unsplash.com/photo-1473966968600-fa801b869a1a?q=80&w=1200",     
    }

    print("Fixing missing category images...")

    for slug, url in fix_data.items():
        trans = CollectionTranslation.objects.filter(slug=slug).first()
        if not trans or not trans.baseid:
            print(f"   ! Could not find collection with slug: {slug}")
            continue

        collection = trans.baseid
        print(f"Updating '{trans.name}'...")

        try:
            upload_result = cloudinary.uploader.upload(
                url,
                folder="categories/fixes/",
                public_id=f"fix_{slug}",
                overwrite=True
            )
            
            cloud_url = upload_result.get('secure_url')

            asset = Asset.objects.create(
                createdat=timezone.now(),
                updatedat=timezone.now(),
                name=f"Fix for {trans.name}",
                type='IMAGE',
                mimetype='image/jpeg',
                source=cloud_url,
                preview=cloud_url
            )

            collection.featuredassetid = asset
            collection.save()
            print(f"   + Successfully assigned image to {trans.name}")

        except Exception as e:
            print(f"   - Failed {slug}: {e}")

if __name__ == "__main__":
    fix_missing_images()

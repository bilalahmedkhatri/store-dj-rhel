import os
import django
import sys
import cloudinary.uploader
import requests
from django.utils import timezone

# Setup Django
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
    print(f"Error: {e}")
    sys.exit(1)

from app.models import Asset, Collection, CollectionTranslation

def update_formal_shirt():
    slug = "seed-formal-shirts"
    
    # List of candidate URLs to try in order
    candidate_urls = [
        "https://images.unsplash.com/photo-1598033129183-c4f50c7176c8?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1621072156002-e2fcced0b170?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=1200&q=80",
        "https://images.unsplash.com/photo-1594932224828-b4b059b6f6ee?auto=format&fit=crop&w=1200&q=80"
    ]

    print(f"Updating image for '{slug}' with robust fallback logic...")

    trans = CollectionTranslation.objects.filter(slug=slug).first()
    if not trans or not trans.baseid:
        print(f"Error: Category with slug '{slug}' not found.")
        return

    collection = trans.baseid
    working_url = None

    # Step 1: Check which URL is reachable
    for url in candidate_urls:
        print(f"Checking URL: {url[:60]}...")
        try:
            resp = requests.head(url, timeout=5, allow_redirects=True)
            if resp.status_code == 200:
                working_url = url
                print("   [Match Found] URL is valid.")
                break
            else:
                print(f"   [Error] Status {resp.status_code}")
        except Exception as e:
            print(f"   [Error] Connection failed: {e}")

    if not working_url:
        print("Fatal: None of the candidate URLs are currently reachable.")
        return

    # Step 2: Upload the working URL
    try:
        print("Uploading to Cloudinary...")
        upload_result = cloudinary.uploader.upload(
            working_url,
            folder="categories/updates/",
            public_id=f"single_fix_{slug}",
            overwrite=True
        )
        
        cloud_url = upload_result.get('secure_url')

        # Step 3: Update DB
        asset = Asset.objects.create(
            createdat=timezone.now(),
            updatedat=timezone.now(),
            name=f"Formal Shirt Cover (Robust)",
            type='IMAGE',
            mimetype='image/jpeg',
            source=cloud_url,
            preview=cloud_url
        )

        collection.featuredassetid = asset
        collection.save()
        
        print(f"Successfully updated '{trans.name}' with verified image: {cloud_url}")

    except Exception as e:
        print(f"Failed during upload process: {e}")

if __name__ == "__main__":
    update_formal_shirt()

#!/usr/bin/env python
"""
Seed storefront categories (Vendure collections), closure rows, channel links,
and collection–variant links so /category/<id>/ pages show products.

Usage:
  python seed.py              # idempotent: create missing seed data, link variants
  python seed.py --reset      # remove seed-* collections then seed again

Requires PostgreSQL env vars (see setup/settings.py) or a working default database.
"""
from __future__ import annotations

import argparse
import os
import sys
import uuid

import django
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

# Project root on path
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")

try:
    from dotenv import load_dotenv

    load_dotenv(os.path.join(ROOT, ".env"))
except ImportError:
    pass

django.setup()

from django.conf import settings
import cloudinary
import cloudinary.uploader
cloudinary.config(
    cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
    api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
    api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
    secure=True
)

from app.models import (  # noqa: E402
    Asset,
    Channel,
    Collection,
    CollectionChannelsChannel,
    CollectionClosure,
    CollectionProductVariantsProductVariant,
    CollectionTranslation,
    Product,
    ProductTranslation,
    ProductVariant,
    ProductVariantPrice,
    ProductVariantTranslation,
)

LANG = "en"
import random

SEED_TRANSLATIONS: list[tuple[str, str, str, str]] = [
    # slug, name, description, role
    ("seed-shop-root", "Shop", "Browse everything we offer.", "root"),
    ("seed-suits", "Premium Suits & Blazers", "Elegant suits and blazers for formal occasions.", "child"),
    ("seed-formal-shirts", "Formal Shirts", "Crisp formal shirts for a professional look.", "child"),
    ("seed-casual-shirts", "Casual Shirts", "Comfortable and stylish casual shirts.", "child"),
    ("seed-tshirts", "T-Shirts & Polos", "Essential t-shirts and polo shirts for everyday wear.", "child"),
    ("seed-hoodies", "Hoodies & Sweatshirts", "Warm and cozy hoodies and sweatshirts.", "child"),
    ("seed-outerwear", "Jackets & Coats", "Stylish jackets and coats for all seasons.", "child"),
    ("seed-eastern", "Traditional Eastern Wear", "Traditional kurtas, shalwar kameez, and more.", "child"),
    ("seed-denim", "Jeans & Denim", "Durable and trendy denim jeans and jackets.", "child"),
    ("seed-chinos", "Chinos & Casual Pants", "Versatile chinos and casual pants.", "child"),
    ("seed-trousers", "Dress Trousers", "Formal dress trousers for a sharp look.", "child"),
    ("seed-shorts", "Shorts", "Comfortable shorts for casual and active wear.", "child"),
    ("seed-activewear", "Activewear & Gym", "High-performance gear for your workouts.", "child"),
    ("seed-innerwear", "Innerwear & Socks", "Comfortable innerwear and essential socks.", "child"),
    ("seed-accessories", "Men's Accessories (Belts & Wallets)", "Premium belts, wallets, and other accessories.", "child"),
]


def add_collection_closure(collection: Collection, parent: Collection | None) -> None:
    """Mirror Vendure: (C,C); plus (A,C) for each (A,P) when parent P is set."""
    CollectionClosure.objects.get_or_create(
        id_ancestor=collection,
        id_descendant=collection,
    )
    if parent is None:
        return
    for row in CollectionClosure.objects.filter(id_descendant=parent).select_related(
        "id_ancestor"
    ):
        CollectionClosure.objects.get_or_create(
            id_ancestor=row.id_ancestor,
            id_descendant=collection,
        )


def delete_seed_collections() -> None:
    """Remove collections whose English slug starts with seed-."""
    seed_trans = CollectionTranslation.objects.filter(slug__startswith="seed-", languagecode=LANG)
    for trans in seed_trans:
        if not trans.baseid:
            continue
        col = trans.baseid
        CollectionProductVariantsProductVariant.objects.filter(collectionid=col).delete()
        CollectionChannelsChannel.objects.filter(collectionid=col).delete()
        CollectionClosure.objects.filter(
            Q(id_ancestor=col) | Q(id_descendant=col)
        ).delete()
        CollectionTranslation.objects.filter(baseid=col).delete()
        cid = col.pk
        col.delete()
        print(f"Removed collection slug={trans.slug} (id was {cid})")


def link_collection_to_default_channel(collection: Collection) -> None:
    channel = Channel.objects.order_by("id").first()
    if not channel:
        print("No Channel row found; skipping collection_channels_channel.")
        return
    CollectionChannelsChannel.objects.get_or_create(
        collectionid=collection,
        defaults={"channelid": channel},
    )


def ensure_demo_asset() -> Asset:
    # Use a high-quality fashion placeholder URL
    remote_url = "https://images.unsplash.com/photo-1594932224828-b4b059b6f6ee?q=80&w=800"
    
    # Check if we already have a cloud asset with this name
    existing = Asset.objects.filter(name="Default Seed Asset").first()
    if existing:
        return existing
        
    print("Uploading default seed asset to Cloudinary...")
    upload_result = cloudinary.uploader.upload(
        remote_url,
        folder="assets/seed/",
        public_id="default_seed_image",
        overwrite=True
    )
    
    cloud_url = upload_result.get('secure_url')
    now = timezone.now()
    return Asset.objects.create(
        createdat=now,
        updatedat=now,
        name="Default Seed Asset",
        type="IMAGE",
        mimetype="image/jpeg",
        width=upload_result.get('width', 800),
        height=upload_result.get('height', 800),
        filesize=upload_result.get('bytes', 0),
        source=cloud_url,
        preview=cloud_url,
    )


def generate_clothing_products():
    base_names = [
        "Slim Fit Kurta", "Classic Shalwar Kameez", "Graphic T-Shirt",
        "Slim Fit Jeans", "Casual Button-Down Shirt", "Cotton Chinos",
        "Performance Polo", "Straight Fit Trousers"
    ]

    products = []
    for i in range(30):
        name = f"{random.choice(base_names)} {i+1}"
        slug = name.lower().replace(" ", "-")
        price = random.randint(1500, 8000)
        products.append((name, slug, "Premium quality fabric and stitching.", price * 100))

    return products


def ensure_demo_products(min_variants: int = 10) -> list[ProductVariant]:
    """Create minimal products/variants if DB has too few."""
    print("Ensuring demo products and variants (Safe Mode A)...")
    now = timezone.now()
    asset = ensure_demo_asset()
    catalog = [
        ("Loewe Inspired Taupe Co-ord Set", "loewe-coord-set", "Premium polyester-viscose blend two-piece set. Features utility pockets and matching trousers.", 1250000),
        ("Oxford Formal Shirt", "formal-shirt-oxford", "Classic white oxford shirt for formal occasions.", 350000),
        ("Slim Fit Navy Blazer", "navy-blazer-slim", "Tailored navy blazer for a sharp professional look.", 850000),
        ("Classic Blue Denim Jacket", "denim-jacket-classic", "Timeless denim jacket with a comfortable fit.", 450000),
        ("Premium Wool Mix Suit", "wool-suit-premium", "High-quality wool blend suit for weddings and events.", 1850000),
        ("Urban Pull-Over Hoodie", "urban-hoodie-gray", "Soft cotton fleece hoodie for casual comfort.", 320000),
        ("Performance Gym Tee", "active-tee-black", "Moisture-wicking fabric for intense workouts.", 220000),
        ("Classic Leather Belt", "leather-belt-brown", "Genuine leather belt with a polished buckle.", 150000),
        ("Cotton Lounge Shorts", "lounge-shorts-navy", "Breathable cotton shorts for relaxed days.", 180000),
    ]

    catalog.extend(generate_clothing_products())

    for name, slug, desc, cents in catalog:
        existing = ProductTranslation.objects.filter(
            slug=slug,
            languagecode=LANG
        ).first()

        if existing:
            product = existing.baseid
            ProductTranslation.objects.filter(
                baseid=product,
                languagecode=LANG
            ).update(
                name=name,
                description=desc,
                updatedat=now
            )
            continue
            
        product = Product.objects.create(
            createdat=now,
            updatedat=now,
            enabled=True,
            featuredassetid=asset,
        )
        ProductTranslation.objects.create(
            createdat=now,
            updatedat=now,
            languagecode=LANG,
            name=name,
            slug=slug,
            description=desc,
            baseid=product,
        )
        variant = ProductVariant.objects.create(
            createdat=now,
            updatedat=now,
            enabled=True,
            sku=f"SEED-{slug.upper()}-{uuid.uuid4().hex[:6]}",
            outofstockthreshold=0,
            useglobaloutofstockthreshold=True,
            trackinventory="FALSE",
            featuredassetid=asset,
            productid=product,
        )
        ProductVariantTranslation.objects.create(
            createdat=now,
            updatedat=now,
            languagecode=LANG,
            name=name,
            baseid=variant,
        )
        ProductVariantPrice.objects.create(
            createdat=now,
            updatedat=now,
            currencycode="PKR",
            channelid=None,
            price=cents,
            variantid=variant,
        )

    return list(
        ProductVariant.objects.filter(
            enabled=True,
            deletedat__isnull=True,
            productid__enabled=True,
            productid__deletedat__isnull=True,
        ).order_by("id")
    )


def ensure_collections() -> dict[str, Collection]:
    now = timezone.now()
    root = None
    collections_map: dict[str, Collection] = {}

    for slug, name, description, role in SEED_TRANSLATIONS:
        collection = None

        trans = CollectionTranslation.objects.filter(
            slug=slug, languagecode=LANG
        ).select_related("baseid").first()

        if trans and trans.baseid:
            collection = trans.baseid

        is_root = role == "root"
        position = 0 if is_root else len(collections_map)
        
        if not is_root and root is None:
            # Try to find existing root if not in current map
            root_trans = CollectionTranslation.objects.filter(slug="seed-shop-root", languagecode=LANG).first()
            if root_trans:
                root = root_trans.baseid
            else:
                raise RuntimeError("Seed root collection missing; run seed in order.")

        parent = None if is_root else root

        if not collection:
            collection = Collection.objects.create(
                createdat=now,
                updatedat=now,
                isroot=is_root,
                position=position,
                isprivate=False,
                filters="[]",
                inheritfilters=False,
                parentid=parent,
                featuredassetid=None,
            )
            add_collection_closure(collection, parent)
            link_collection_to_default_channel(collection)

        CollectionTranslation.objects.update_or_create(
            baseid=collection,
            languagecode=LANG,
            defaults={
                "name": name,
                "slug": slug,
                "description": description,
                "updatedat": now,
            },
        )

        collections_map[slug] = collection
        if is_root:
            root = collection
        print(f'Ensured collection "{name}" slug={slug} id={collection.id}')

    return collections_map


def link_variants_to_categories(
    collections_map: dict[str, Collection],
    variants: list[ProductVariant],
) -> None:
    if not variants:
        print("No variants to link; category pages will stay empty.")
        return

    linked = 0
    for v in variants:
        v_trans = ProductVariantTranslation.objects.filter(baseid=v, languagecode=LANG).first()
        if not v_trans: continue
        
        target_slugs = []
        name_lower = v_trans.name.lower()
        
        # Mapping Logic
        if "kurta" in name_lower or "shalwar" in name_lower or "eastern" in name_lower:
            target_slugs.append("seed-eastern")
        
        if "suit" in name_lower or "blazer" in name_lower or "loewe" in name_lower:
            target_slugs.append("seed-suits")
            
        if "formal shirt" in name_lower:
            target_slugs.append("seed-formal-shirts")
        elif "shirt" in name_lower:
            target_slugs.append("seed-casual-shirts")
            
        if "jeans" in name_lower or "denim" in name_lower:
            target_slugs.append("seed-denim")
            
        if "t-shirt" in name_lower or "polo" in name_lower or "tee" in name_lower:
            target_slugs.append("seed-tshirts")
            
        if "jacket" in name_lower or "coat" in name_lower or "outerwear" in name_lower:
            target_slugs.append("seed-outerwear")
            
        if "pant" in name_lower or "chino" in name_lower:
            target_slugs.append("seed-chinos")
            
        if "trouser" in name_lower:
            target_slugs.append("seed-trousers")

        if "hoodie" in name_lower or "sweatshirt" in name_lower:
            target_slugs.append("seed-hoodies")

        if "short" in name_lower:
            target_slugs.append("seed-shorts")

        if "activewear" in name_lower or "gym" in name_lower or "sport" in name_lower:
            target_slugs.append("seed-activewear")

        if "innerwear" in name_lower or "socks" in name_lower or "brief" in name_lower:
            target_slugs.append("seed-innerwear")

        if "belt" in name_lower or "wallet" in name_lower or "accessory" in name_lower or "accessories" in name_lower:
            target_slugs.append("seed-accessories")
        
        # Deduplicate and Link
        for target_slug in set(target_slugs):
            if target_slug in collections_map:
                col = collections_map[target_slug]
                _, created = CollectionProductVariantsProductVariant.objects.get_or_create(
                    collectionid=col,
                    productvariantid=v,
                )
                if created: linked += 1
            
        # Also link to root Shop
        if "seed-shop-root" in collections_map:
            _, created_root = CollectionProductVariantsProductVariant.objects.get_or_create(
                collectionid=collections_map["seed-shop-root"],
                productvariantid=v,
            )
            if created_root: linked += 1

    print(f"Linked {linked} collection-variant rows.")


def run_seed(*, reset: bool) -> None:
    with transaction.atomic():
        if reset:
            delete_seed_collections()
        collections_map = ensure_collections()
        variants = ensure_demo_products(min_variants=8)
        link_variants_to_categories(collections_map, variants)

    # Print URLs
    for slug, col in collections_map.items():
        if slug == "seed-shop-root": continue
        print(f"Category: {slug} -> /category/{col.id}/")


def main() -> None:
    p = argparse.ArgumentParser(description="Seed Vendure-style collections for the storefront.")
    p.add_argument(
        "--reset",
        action="store_true",
        help="Delete seed-* collections (and their links) before seeding.",
    )
    args = p.parse_args()
    run_seed(reset=args.reset)


if __name__ == "__main__":
    main()

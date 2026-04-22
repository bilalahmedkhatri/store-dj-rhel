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
    ("seed-electronics", "Electronics", "Gadgets, smartphones, and latest tech accessories.", "child"),
    ("seed-fashion", "Fashion", "Trendy clothing, footwear, and stylish accessories for all.", "child"),
    ("seed-home-kitchen", "Home & Kitchen", "Essential appliances, decor, and kitchenware for your home.", "child"),
    ("seed-beauty-health", "Beauty & Health", "Skincare, makeup, and wellness products.", "child"),
    ("seed-sports-outdoors", "Sports & Outdoors", "Gear for fitness, camping, and athletic performance.", "child"),
    ("seed-men-eastern", "Men Eastern", "Traditional eastern wear for men.", "child"),
    ("seed-men-western", "Men Western", "Western wear for men.", "child"),
    ("seed-boys-western", "Boys Western", "Modern western wear for boys.", "child"),
    ("seed-girls-western", "Girls Western", "Modern western wear for girls.", "child"),
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
    preview = "/static/images/products/product.jpg"
    existing = Asset.objects.filter(preview=preview).order_by("id").first()
    if existing:
        return existing
    now = timezone.now()
    return Asset.objects.create(
        createdat=now,
        updatedat=now,
        name="Seed storefront image",
        type="IMAGE",
        mimetype="image/jpeg",
        width=800,
        height=800,
        filesize=1,
        source=preview,
        preview=preview,
    )


def generate_clothing_products():
    base_names = [
        "Men Kurta", "Men Shalwar Kameez", "Men T-Shirt",
        "Men Jeans", "Boys Kurta", "Girls Frock",
        "Kids T-Shirt", "Kids Jeans"
    ]

    products = []
    for i in range(30):
        name = f"{random.choice(base_names)} {i+1}"
        slug = name.lower().replace(" ", "-")
        price = random.randint(1000, 5000)
        products.append((name, slug, "High quality fabric", price * 100))

    return products


def ensure_demo_products(min_variants: int = 10) -> list[ProductVariant]:
    """Create minimal products/variants if DB has too few."""
    print("Ensuring demo products and variants (Safe Mode A)...")
    now = timezone.now()
    asset = ensure_demo_asset()
    catalog = [
        ("Wireless Headphones", "electronics-headphones", "Rich sound, clear mic.", 1200000),
        ("Smart Watch", "electronics-watch", "Track fitness and notifications.", 850000),
        ("Cotton T-Shirt", "fashion-tee", "Soft and breathable cotton.", 150000),
        ("Denim Jacket", "fashion-denim", "Classic style for all seasons.", 450000),
        ("Air Fryer", "home-fryer", "Healthy cooking with less oil.", 1800000),
        ("Coffee Maker", "home-coffee", "Start your morning with fresh brew.", 950000),
        ("Vitamin C Serum", "beauty-serum", "For glowing and healthy skin.", 250000),
        ("Yoga Mat", "sports-mat", "Non-slip grip for your workouts.", 300000),
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
        
        target_slug = None
        name_lower = v_trans.name.lower()
        if "kurta" in name_lower or "shalwar" in name_lower:
            target_slug = "seed-men-eastern"
        elif "boy" in name_lower or "kids jeans" in name_lower or "kids t-shirt" in name_lower:
            target_slug = "seed-boys-western"
        elif "girl" in name_lower or "frock" in name_lower:
            target_slug = "seed-girls-western"
        elif "jeans" in name_lower or "t-shirt" in name_lower:
            target_slug = "seed-men-western"
        elif "electronics" in name_lower or "watch" in name_lower or "headphone" in name_lower:
            target_slug = "seed-electronics"
        elif "fashion" in name_lower or "shirt" in name_lower or "jacket" in name_lower:
            target_slug = "seed-fashion"
        elif "home" in name_lower or "fryer" in name_lower or "coffee" in name_lower:
            target_slug = "seed-home-kitchen"
        elif "beauty" in name_lower or "serum" in name_lower:
            target_slug = "seed-beauty-health"
        elif "sports" in name_lower or "mat" in name_lower:
            target_slug = "seed-sports-outdoors"
        
        if target_slug and target_slug in collections_map:
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

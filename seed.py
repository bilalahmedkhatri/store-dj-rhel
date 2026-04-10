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
SEED_TRANSLATIONS: list[tuple[str, str, str, str]] = [
    # slug, name, description, position under parent (root first)
    ("seed-shop-root", "Shop", "Browse everything we offer.", "root"),
    ("seed-electronics", "Electronics", "Gadgets and tech.", "child"),
    ("seed-apparel", "Apparel", "Clothing and accessories.", "child"),
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
    """Remove collections whose English slug is seed-* (children before root)."""
    slugs_ordered = ["seed-apparel", "seed-electronics", "seed-shop-root"]
    for slug in slugs_ordered:
        trans = CollectionTranslation.objects.filter(
            slug=slug, languagecode=LANG
        ).first()
        if not trans or not trans.baseid_id:
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
        print(f"Removed collection slug={slug} (id was {cid})")


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


def ensure_demo_products(min_variants: int = 4) -> list[ProductVariant]:
    """Create minimal products/variants if DB has too few."""
    existing = list(
        ProductVariant.objects.filter(
            enabled=True,
            deletedat__isnull=True,
            productid__enabled=True,
            productid__deletedat__isnull=True,
        ).order_by("id")[: max(min_variants, 8)]
    )
    if len(existing) >= min_variants:
        return existing

    print("Creating demo products and variants for seeding…")
    now = timezone.now()
    asset = ensure_demo_asset()
    catalog = [
        ("Seed Tee", "seed-tee", "Soft cotton tee.", 2499),
        ("Seed Hoodie", "seed-hoodie", "Warm hoodie.", 5999),
        ("Seed Cap", "seed-cap", "Adjustable cap.", 1499),
        ("Seed Tote", "seed-tote", "Canvas tote.", 1999),
    ]

    for name, slug, desc, cents in catalog:
        if ProductTranslation.objects.filter(slug=slug, languagecode=LANG).exists():
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
        ).order_by("id")[: max(min_variants, 8)]
    )


def ensure_collections() -> tuple[Collection, Collection, Collection]:
    now = timezone.now()
    root = None
    children: list[Collection] = []

    for slug, name, description, role in SEED_TRANSLATIONS:
        trans = CollectionTranslation.objects.filter(
            slug=slug, languagecode=LANG
        ).first()
        if trans and trans.baseid:
            col = trans.baseid
            if role == "root":
                root = col
            else:
                children.append(col)
            continue

        parent = None
        is_root = role == "root"
        position = 0 if is_root else len(children)
        if not is_root and root is None:
            raise RuntimeError("Seed root collection missing; run seed in order.")

        if not is_root:
            parent = root

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
        CollectionTranslation.objects.create(
            createdat=now,
            updatedat=now,
            languagecode=LANG,
            name=name,
            slug=slug,
            description=description,
            baseid=collection,
        )
        add_collection_closure(collection, parent)
        link_collection_to_default_channel(collection)

        if is_root:
            root = collection
        else:
            children.append(collection)
        print(f'Created collection "{name}" slug={slug} id={collection.id}')

    if root is None or len(children) < 2:
        raise RuntimeError("Failed to resolve root + two child collections.")
    return root, children[0], children[1]


def link_variants_to_categories(
    electronics: Collection,
    apparel: Collection,
    variants: list[ProductVariant],
) -> None:
    if not variants:
        print("No variants to link; category pages will stay empty.")
        return
    mid = max(1, len(variants) // 2)
    bucket_e = variants[:mid]
    bucket_a = variants[mid:] if len(variants) > mid else variants[:mid]

    linked = 0
    for col, bucket in ((electronics, bucket_e), (apparel, bucket_a)):
        for v in bucket:
            _, created = CollectionProductVariantsProductVariant.objects.get_or_create(
                collectionid=col,
                productvariantid=v,
            )
            if created:
                linked += 1
    print(f"Linked {linked} new collection-variant rows (skipped existing pairs).")


def run_seed(*, reset: bool) -> None:
    with transaction.atomic():
        if reset:
            delete_seed_collections()
        root, electronics, apparel = ensure_collections()
        variants = ensure_demo_products(min_variants=4)
        link_variants_to_categories(electronics, apparel, variants)

    # Print URLs (slug route optional)
    for slug in ("seed-electronics", "seed-apparel"):
        t = CollectionTranslation.objects.filter(slug=slug, languagecode=LANG).first()
        if t and t.baseid:
            cid = t.baseid_id
            print(
                f"Open category: /category/{cid}/ or /category/{cid}/{t.slug}/"
            )


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

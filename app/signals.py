import django.dispatch
from django.dispatch import receiver
from .utils import send_order_confirmation_email
import threading

from django.db.models.signals import post_save
from .models import Asset, Product, SearchIndexItem, ProductVariant, Fulfillment
import threading

# Define custom signal
order_confirmed = django.dispatch.Signal()

@receiver(order_confirmed)
def handle_order_confirmation(sender, **kwargs):
    """
    Signal receiver that sends the confirmation email.
    Uses threading to ensure it doesn't block the HTTP response.
    """
    user_email = kwargs.get('user_email')
    context = kwargs.get('context')
    
    if user_email and context:
        # Run in a separate thread to send the response to the user immediately
        email_thread = threading.Thread(
            target=send_order_confirmation_email, 
            args=(user_email, context)
        )
        email_thread.start()

@receiver(post_save, sender=Product)
@receiver(post_save, sender=ProductVariant)
def update_search_index(sender, instance, **kwargs):
    """
    Update SearchIndexItem when a product or variant is saved.
    This keeps the frontend search denormalized table in sync.
    """
    def run_index_update():
        try:
            # If it's a product, we might want to update all its variants
            if isinstance(instance, Product):
                variants = ProductVariant.objects.filter(productid=instance)
            else:
                variants = [instance]

            for variant in variants:
                product = variant.productid
                trans = variant.productvarianttranslation_set.filter(languagecode='en').first()
                p_trans = product.producttranslation_set.filter(languagecode='en').first()
                
                if not p_trans: continue

                # Update or create search index entry
                # Note: This is simplified; Vendure's search index handles channels, facets, etc.
                SearchIndexItem.objects.update_or_create(
                    productvariantid=variant.id,
                    languagecode='en',
                    defaults={
                        'productname': p_trans.name,
                        'productvariantname': trans.name if trans else p_trans.name,
                        'description': p_trans.description,
                        'slug': p_trans.slug,
                        'sku': variant.sku,
                        'enabled': product.enabled and variant.enabled,
                        'price': variant.get_price(), # Assuming we added get_price helper
                        'pricewithtax': variant.get_price(),
                    }
                )
        except Exception as e:
            print(f"Search index update failed: {e}")

    threading.Thread(target=run_index_update).start()

@receiver(post_save, sender=Asset)
def optimize_asset_image(sender, instance, created, **kwargs):
    """
    Background task to optimize images when an Asset is uploaded.
    """
    if created and instance.mimetype.startswith('image/'):
        def run_optimization():
            try:
                from PIL import Image
                import os
                
                # Assuming 'source' is a file path or URL
                # In this hybrid setup, we need to be careful with paths
                if os.path.exists(instance.source):
                    img = Image.open(instance.source)
                    # Convert to WebP if not already
                    if not instance.source.endswith('.webp'):
                        webp_path = os.path.splitext(instance.source)[0] + '.webp'
                        img.save(webp_path, 'WEBP', quality=80)
                        # Optionally update instance with new path
            except ImportError:
                pass
            except Exception as e:
                print(f"Image optimization failed: {e}")

        threading.Thread(target=run_optimization).start()

@receiver(post_save, sender=Fulfillment)
def handle_stock_sync(sender, instance, **kwargs):
    """
    Sync stock when a fulfillment is updated.
    """
    if instance.state == 'Shipped':
        def sync_stock():
            print(f"Syncing stock for fulfillment {instance.id}")
            # Logic to decrement StockOnHand and StockAllocated
            pass
        
        threading.Thread(target=sync_stock).start()

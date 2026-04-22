from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
import uuid

def send_order_confirmation_email(user_email, context):
    """
    Sends a modern HTML order confirmation email to the user.
    'context' should contain: user_name, order_id, cart_items, subtotal, shipping, total, address, phone, payment_method, etc.
    """
    subject = f'Order Confirmation - {context.get("order_id", "#12345")}'
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@storedjreheel.com')
    to = [user_email]

    # Generate unique order ID if not provided
    if "order_id" not in context:
        context["order_id"] = str(uuid.uuid4().hex[:8]).upper()

    html_content = render_to_string('emails/order_confirmation.html', context)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    
    try:
        msg.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_merchant_welcome_email(user_email, context):
    """
    Sends a welcome email to verified merchants.
    'context' should contain: merchant_name, merchant_id, merchant_type, verification_date, dashboard_url
    """
    subject = 'Welcome to e-sahulat - Your Merchant Account is Verified!'
    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@storedjreheel.com')
    to = [user_email]

    html_content = render_to_string('emails/merchant_welcome.html', context)
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    
    try:
        msg.send()
        return True
    except Exception as e:
        print(f"Error sending merchant welcome email: {e}")
        return False

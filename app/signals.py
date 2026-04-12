import django.dispatch
from django.dispatch import receiver
from .utils import send_order_confirmation_email
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

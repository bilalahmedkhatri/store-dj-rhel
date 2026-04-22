import json
import hashlib
import hmac
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
import os

def verify_signature(payload_body, signature_header):
    """
    Verify the HMAC-SHA256 signature from GoPayFast.
    """
    secret = os.environ.get("PAYFAST_SECURED_KEY", "YOUR_SECURED_KEY")
    if not signature_header:
        return False
    
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload_body,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_signature, signature_header)

@csrf_exempt
@require_POST
def gopayfast_webhook(request):
    """
    Handle incoming webhooks from GoPayFast.
    """
    signature = request.headers.get('X-PayFast-Signature')
    
    if not verify_signature(request.body, signature):
        # In production, we should log this attempt
        return HttpResponseBadRequest("Invalid signature")

    try:
        data = json.loads(request.body)
        event_type = data.get('event')
        payload = data.get('data', {})

        if event_type == 'payment.success':
            handle_payment_success(payload)
        elif event_type == 'payment.failed':
            handle_payment_failed(payload)
        elif event_type == 'refund.processed':
            handle_refund_processed(payload)
        
        return HttpResponse("Webhook processed", status=200)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")
    except Exception as e:
        # Log the error
        return HttpResponse(f"Error processing webhook: {str(e)}", status=500)

def handle_payment_success(data):
    # Update order status in database
    # transaction_id = data.get('transaction_id')
    # order = Order.objects.get(transaction_id=transaction_id)
    # order.status = 'PAID'
    # order.save()
    pass

def handle_payment_failed(data):
    # Update order status or notify user
    pass

def handle_refund_processed(data):
    # Update refund status
    pass

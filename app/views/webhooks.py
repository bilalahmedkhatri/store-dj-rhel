import json
import hashlib
import hmac
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings

@csrf_exempt
@require_POST
def gopayfast_webhook(request):
    """
    Handle incoming webhooks from GoPayFast.
    """
    # In a real scenario, verify the signature/checksum
    # signature = request.headers.get('X-PayFast-Signature')
    # if not verify_signature(request.body, signature):
    #     return HttpResponseBadRequest("Invalid signature")

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
    except Exception as e:
        # Log the error
        return HttpResponse("Error processing webhook", status=500)

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

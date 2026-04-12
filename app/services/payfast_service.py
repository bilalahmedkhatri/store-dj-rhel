import urllib.parse
import requests
import os
from django.utils import timezone

# PayFast (GoToPayFast) Configuration
# https://www.gotopayfast.com/
PAYFAST_MERCHANT_ID = os.environ.get("PAYFAST_MERCHANT_ID", "YOUR_MERCHANT_ID")
PAYFAST_SECURED_KEY = os.environ.get("PAYFAST_SECURED_KEY", "YOUR_SECURED_KEY")

PAYFAST_URL = os.getenv('PAYFAST_URL')
PAYFAST_SANDBOX_URL = os.getenv('PAYFAST_SANDBOX_URL')
IS_TEST_MODE = True # Set to False in production

def get_payfast_url():
    return PAYFAST_SANDBOX_URL if IS_TEST_MODE else PAYFAST_URL

def generate_payfast_checkout_url(order_id, amount, email, phone, return_url):
    """
    Generates the payment link for PayFast Gateway which supports:
    - Master/Visa Cards
    - Bank Transfers
    - Mobile Wallets (Easypaisa, JazzCash, Upaisa)
    """
    base_url = get_payfast_url()
    
    # Setup PayFast Payload
    # PayFast requires specific token generation or parameterized secure keys 
    # depending on their latest API v2. Typically passed as POST or GET param.
    payload = {
        "MERCHANT_ID": PAYFAST_MERCHANT_ID,
        "SECURED_KEY": PAYFAST_SECURED_KEY,
        "TXNAMT": str(amount),
        "CUSTOMER_EMAIL_ADDRESS": email,
        "CUSTOMER_MOBILE_NO": phone,
        "TXNDESC": f"Payment for Order #{order_id}",
        "SUCCESS_URL": return_url,
        "FAILURE_URL": return_url,
        "CHECKOUT_URL": return_url,
        "BASKET_ID": order_id,
        "ORDER_DATE": timezone.now(), # Example format
    }

    # Usually, PayFast expects a POST request to their hosted page, but some merchants
    # generate a redirect token first via a Server-to-Server call:
    try:
        # NOTE: If Server-to-Server flow is preferred:
        token_request = requests.post(
            f"{base_url}/initiate", 
            json=payload,
            timeout=10
        )
        if token_request.status_code == 200:
            token_data = token_request.json()
            redirect_url = token_data.get("redirect_url")
            return redirect_url
    except Exception as e:
        print(f"PayFast integration warning: {e}")
        pass

    # Fallback to direct GET format if applicable (Simplified reference)
    qs = urllib.parse.urlencode(payload)
    return f"{base_url}?{qs}"

def verify_payfast_callback(request_data):
    """
    Called via the Webhook or Success Redirect from PayFast to verify the transaction.
    """
    transaction_id = request_data.get("TRANSACTION_ID")
    status = request_data.get("TXN_STATUS")
    
    if status == "SUCCESS":
        # Additional cryptographic verification against your backend
        return True, "Payment Successful", transaction_id
    elif status == "FAILED":
        return False, "Payment Failed", transaction_id
    
    return False, "Unknown Status", transaction_id

# -------------------------------------------------------------
# Safepay Alternative Integration 
# -------------------------------------------------------------
def generate_safepay_checkout_url(order_id, amount, currency="PKR"):
    """
    Safepay is another highly reliable Y-Combinator backed gateway in Pakistan.
    Provides a beautiful checkout modal.
    """
    from safepay import Safepay # pip install safepay-python
    
    env = "sandbox" if IS_TEST_MODE else "production"
    sf_key = os.environ.get("SAFEPAY_API_KEY")
    
    safepay = Safepay({
        'environment': env,
        'apiKey': sf_key,
        'v1Secret': 'secret',
        'webhookSecret': 'secret'
    })
    
    # 1. Provide total amount to be charged 
    # 2. Get a secure Tracker token
    tracker = safepay.checkout.create({
        "amount": amount,
        "currency": currency,
        "cancel_url": f"http://yoursite.com/cancel/{order_id}",
        "redirect_url": f"http://yoursite.com/success/{order_id}"
    })
    
    # 3. Construct checkout URL
    checkout_url = f"https://sandbox.api.getsafepay.com/checkout/pay?tracker={tracker['tracker']}"
    return checkout_url

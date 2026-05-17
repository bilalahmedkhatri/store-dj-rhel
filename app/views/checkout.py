from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
import uuid
import json

from ..models import User as AppUser, Customer, Address, Order, OrderLine, ProductVariant, ProductTranslation
from .cart_utils import CART_SESSION_KEY, build_cart_context, get_cart

def checkout_view(request):
    if request.method == "POST":
        cart = get_cart(request)
        if not cart:
            return redirect("cart")

        # 1. Handle Customer
        customer = None
        if request.user.is_authenticated:
            app_user = AppUser.objects.filter(id=request.user.id).first()
            customer, _ = Customer.objects.get_or_create(
                userid=app_user,
                defaults={
                    'emailaddress': request.user.email,
                    'firstname': request.user.first_name or request.user.username,
                    'lastname': request.user.last_name or ""
                }
            )
        
        # 2. Build Cart Context for totals
        cart_data = build_cart_context(request)
        
        # 3. Create Order
        order_code = uuid.uuid4().hex[:12].upper()
        order = Order.objects.create(
            createdat=timezone.now(),
            updatedat=timezone.now(),
            type='Regular',
            code=order_code,
            state='PaymentSettled', # Mark as settled for demo purposes
            active=True,
            orderplacedat=timezone.now(),
            customerid=customer,
            currencycode='PKR',
            subtotal=int(cart_data['subtotal'] * 100),
            subtotalwithtax=int((cart_data['subtotal'] + cart_data['tax']) * 100),
            shipping=int(cart_data['shipping'] * 100),
            shippingwithtax=int(cart_data['shipping'] * 100),
            couponcodes="[]",
            shippingaddress=json.dumps({
                "fullName": request.POST.get('first_name', '') + " " + request.POST.get('last_name', ''),
                "streetLine1": request.POST.get('address', ''),
                "city": request.POST.get('city', ''),
                "postalCode": request.POST.get('postal', ''),
                "countryCode": request.POST.get('country', 'PK')
            }),
            billingaddress="{}"
        )

        # 4. Create OrderLines
        for item in cart:
            # Try to find the variant
            variant = ProductVariant.objects.filter(sku=item['slug']).first()
            if not variant:
                # Fallback: find by name
                variant = ProductVariant.objects.filter(productvarianttranslation__name=item['name']).first()

            OrderLine.objects.create(
                createdat=timezone.now(),
                updatedat=timezone.now(),
                quantity=item['quantity'],
                orderplacedquantity=item['quantity'],
                listpriceincludestax=True,
                adjustments="[]",
                taxlines="[]",
                listprice=int(item['price'] * 100),
                productvariantid=variant if variant else ProductVariant.objects.first(), # Fallback to first if not found
                orderid=order
            )

        # 5. Clear Cart
        request.session[CART_SESSION_KEY] = []
        request.session.modified = True
        
        return redirect("payment_success")

    context = build_cart_context(request)
    
    if request.user.is_authenticated:
        app_user = AppUser.objects.filter(id=request.user.id).first()
        customer = Customer.objects.filter(userid=app_user).first()
        if customer:
            context['saved_customer'] = customer
            # Get default shipping address
            address = Address.objects.filter(customerid=customer, defaultshippingaddress=True).first()
            if address:
                context['saved_address'] = address
                
    return render(request, "landing/checkout.html", context)

def payment_success_view(request):
    # In a real app, we'd fetch transaction details from session or DB
    context = {
        'transaction_id': 'PF-TXN-' + uuid.uuid4().hex[:8].upper(),
        'amount': 'Calculated at checkout',
        'timestamp': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
    }
    return render(request, "landing/payment_success.html", context)

def payment_failed_view(request):
    context = {
        'reason': 'Insufficient funds or transaction declined by bank.',
        'auto_refund_notice': 'If amount was deducted, it will be auto-refunded within 7 days.',
    }
    return render(request, "landing/payment_failed.html", context)

def payment_pending_view(request):
    context = {
        'transaction_ref': 'REF-' + uuid.uuid4().hex[:8].upper(),
    }
    return render(request, "landing/payment_pending.html", context)

def receipt_view(request, transaction_id):
    # Fetch order by code
    order = Order.objects.filter(code=transaction_id).first()
    
    context = {
        'transaction_id': transaction_id,
        'amount': f"{order.subtotal / 100:,.2f}" if order else "0.00",
        'payer_name': order.customerid.firstname if order and order.customerid else "Valued Customer",
        'timestamp': order.createdat.strftime('%Y-%m-%d %H:%M:%S') if order else timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        'order': order
    }
    return render(request, "landing/receipt.html", context)

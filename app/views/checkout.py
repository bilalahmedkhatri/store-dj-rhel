from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
import uuid
import json

from ..models import User as AppUser, Customer, Address, Order, OrderLine, ProductVariant, ProductTranslation
from .cart_utils import CART_SESSION_KEY, build_cart_context, get_cart

def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('/register/?next=/cart/')
        
    if request.method == "POST":
        cart = get_cart(request)
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.POST.get('ajax') == 'true'
        if not cart:
            if is_ajax:
                from django.http import JsonResponse
                return JsonResponse({'status': 'error', 'message': 'Cart is empty', 'redirect_url': '/cart/'})
            return redirect("cart")

        # 1. Handle Customer
        customer = None
        if request.user.is_authenticated:
            app_user = AppUser.objects.filter(identifier=request.user.email).first()
            if not app_user:
                app_user = AppUser.objects.filter(id=request.user.id).first()
                
            if app_user:
                customer = Customer.objects.filter(userid=app_user).first()
                
            if not customer and request.user.email:
                customer = Customer.objects.filter(emailaddress=request.user.email).first()
                
            if not customer:
                customer = Customer.objects.create(
                    userid=app_user,
                    emailaddress=request.user.email,
                    firstname=request.POST.get('first_name', '') or request.user.first_name or "Valued Customer",
                    lastname=request.POST.get('last_name', '') or request.user.last_name or "",
                    phonenumber=request.POST.get('phone', '')
                )
            else:
                # Update details if provided
                if app_user and not customer.userid:
                    customer.userid = app_user
                if request.POST.get('first_name'):
                    customer.firstname = request.POST.get('first_name')
                if request.POST.get('last_name'):
                    customer.lastname = request.POST.get('last_name')
                if request.POST.get('phone'):
                    customer.phonenumber = request.POST.get('phone')
                customer.save()
        else:
            # Guest or anonymous
            email = request.POST.get('email')
            if email:
                customer = Customer.objects.filter(emailaddress=email).first()
            if not customer:
                customer = Customer.objects.create(
                    emailaddress=email,
                    firstname=request.POST.get('first_name', '') or "Valued Customer",
                    lastname=request.POST.get('last_name', '') or "",
                    phonenumber=request.POST.get('phone', '')
                )
            else:
                if request.POST.get('first_name'):
                    customer.firstname = request.POST.get('first_name')
                if request.POST.get('last_name'):
                    customer.lastname = request.POST.get('last_name')
                if request.POST.get('phone'):
                    customer.phonenumber = request.POST.get('phone')
                customer.save()
        
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

        # Create Payment Record
        from ..models import Payment
        payment_method = request.POST.get('payment', 'card')
        Payment.objects.create(
            createdat=timezone.now(),
            updatedat=timezone.now(),
            method=payment_method,
            state='Settled',
            transactionid=order.code,
            amount=int(cart_data['total'] * 100),
            orderid=order,
            metadata="{}"
        )

        # Save order code in session
        request.session['latest_order_code'] = order.code

        # 5. Clear Cart
        request.session[CART_SESSION_KEY] = []
        request.session.modified = True
        
        if is_ajax:
            from django.http import JsonResponse
            return JsonResponse({
                'status': 'success',
                'redirect_url': '/payment/success/',
                'message': 'Order placed successfully!'
            })
            
        return redirect("payment_success")

    context = build_cart_context(request)
    context['saved_customer'] = {
        'emailaddress': '',
        'firstname': '',
        'lastname': '',
        'phonenumber': ''
    }
    context['saved_address'] = {
        'phonenumber': '',
        'streetline1': '',
        'city': '',
        'postalcode': ''
    }
    
    if request.user.is_authenticated:
        app_user = AppUser.objects.filter(identifier=request.user.email).first()
        if not app_user:
            app_user = AppUser.objects.filter(id=request.user.id).first()
            
        customer = None
        if app_user:
            customer = Customer.objects.filter(userid=app_user).first()
            
        # Fallback: find by email ONLY if it matches the current user's email
        if not customer:
            customer = Customer.objects.filter(emailaddress=request.user.email).first()
            
        if customer:
            context['saved_customer'] = customer
            # Get default shipping address
            address = Address.objects.filter(customerid=customer, defaultshippingaddress=True).first()
            if address:
                context['saved_address'] = address
                
    return render(request, "landing/checkout.html", context)

def payment_success_view(request):
    latest_code = request.session.get('latest_order_code')
    order = None
    if latest_code:
        order = Order.objects.filter(code=latest_code).first()
        
    if order:
        from ..models import Payment
        payment = Payment.objects.filter(orderid=order).first()
        amount_paid = f"{(payment.amount / 100) if payment else ((order.subtotalwithtax + order.shipping) / 100):,.2f}"
        context = {
            'transaction_id': order.code,
            'amount': amount_paid,
            'timestamp': order.createdat.strftime('%Y-%m-%d %H:%M:%S'),
        }
    else:
        context = {
            'transaction_id': 'PF-TXN-' + uuid.uuid4().hex[:8].upper(),
            'amount': '0.00',
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
    payment = None
    if order:
        from ..models import Payment
        payment = Payment.objects.filter(orderid=order).first()
        
    payment_via = "ATM Card"
    if payment:
        if payment.method == 'card':
            payment_via = "Credit / Debit Card"
        elif payment.method == 'paypal':
            payment_via = "PayPal"
        else:
            payment_via = payment.method.title()
            
    # Format total paid amount
    total_amount = "0.00"
    if payment:
        total_amount = f"{payment.amount / 100:,.2f}"
    elif order:
        total_amount = f"{(order.subtotalwithtax + order.shipping) / 100:,.2f}"
        
    context = {
        'transaction_id': transaction_id,
        'amount': total_amount,
        'payer_name': order.customerid.firstname if order and order.customerid else "Valued Customer",
        'timestamp': order.createdat.strftime('%Y-%m-%d %H:%M:%S') if order else timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
        'payment_via': payment_via,
        'order': order
    }
    return render(request, "landing/receipt.html", context)

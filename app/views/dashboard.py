from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Customer, Order, Address, ProductVariantPrice
from ..forms import AddressForm

def get_customer_for_user(request):
    from ..models import User as AppUser
    app_user = AppUser.objects.filter(identifier=request.user.email).first()
    if not app_user:
        app_user = AppUser.objects.filter(id=request.user.id).first()
        
    customer = None
    if app_user:
        customer = Customer.objects.filter(userid=app_user).first()
        
    if not customer and request.user.email:
        customer = Customer.objects.filter(emailaddress=request.user.email).first()
        
    if not customer:
        customer = Customer.objects.create(
            userid=app_user,
            emailaddress=request.user.email or f"{request.user.username}@example.com",
            firstname=request.user.first_name or request.user.username,
            lastname=request.user.last_name or ""
        )
    elif app_user and not customer.userid:
        customer.userid = app_user
        customer.save()
        
    return customer

@login_required
def dashboard_view(request):
    """
    Renders a clean, professional dashboard for the authenticated customer.
    """
    # 1. Get or create Customer profile
    customer = get_customer_for_user(request)

    # 2. Get Order History (Recent first)
    orders_qs = Order.objects.filter(customerid=customer).order_by('-createdat')
    orders = []
    for order in orders_qs[:5]: # Show last 5 on overview
        orders.append({
            'code': order.code,
            'date': order.createdat,
            'state': order.state,
            'total': order.subtotal / 100, # Assuming subtotal is in cents
            'items_count': order.orderline_set.count()
        })

    # 3. Get Saved Addresses
    addresses = Address.objects.filter(customerid=customer)

    # 4. Simple Insights
    insights = {
        'total_orders': orders_qs.count(),
        'member_since': customer.createdat,
        'default_address': addresses.filter(defaultshippingaddress=True).first()
    }

    context = {
        'customer': customer,
        'orders': orders,
        'addresses': addresses,
        'insights': insights,
        'active_tab': 'overview'
    }
    
    return render(request, 'landing/dashboard.html', context)

@login_required
def profile_view(request):
    """
    Renders and handles updates for the user profile page.
    """
    customer = get_customer_for_user(request)
    
    # Get default address for editing
    address = Address.objects.filter(customerid=customer, defaultshippingaddress=True).first()
    
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            profile_address = form.save(commit=False)
            profile_address.customerid = customer
            profile_address.defaultshippingaddress = True # Ensure it stays default
            
            # Unset other defaults if this one is set
            Address.objects.filter(customerid=customer, defaultshippingaddress=True).exclude(pk=profile_address.pk).update(defaultshippingaddress=False)
            
            profile_address.save()
            messages.success(request, "Profile details updated successfully.")
            return redirect('profile')
    else:
        form = AddressForm(instance=address)
    
    context = {
        'customer': customer,
        'form': form,
        'address': address,
        'user': request.user
    }
    return render(request, 'landing/profile.html', context)

@login_required
def add_address_view(request):
    """
    Allows a customer to add or update their profile/address details (Redirects to profile).
    """
    return redirect('profile')

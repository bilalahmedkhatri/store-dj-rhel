from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from .mock_data import (
    get_mock_about_data,
    get_mock_contact_data,
    get_mock_payment_methods_data,
    get_mock_privacy_policy_data,
    get_mock_refund_policy_data,
    get_mock_shipping_policy_data,
    get_mock_terms_data,
)


def faqs(request):
    return render(request, 'landing/faq.html')

def about_us(request):
    return render(request, 'landing/about.html', get_mock_about_data())

def contact_us(request):
    context = get_mock_contact_data()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        # Send email (configure settings first)
        send_mail(
            f'Contact Form: {subject}',
            f'From: {name} <{email}>\n\n{message}',
            email,
            ['support@azeemlab.com'],
            fail_silently=False,
        )
        messages.success(request, 'Your message has been sent. We\'ll get back to you soon.')
        return redirect('contact_us')
    return render(request, 'landing/contact.html', context)
def privacy_policy(request):
    return render(request, 'landing/privacy.html', get_mock_privacy_policy_data())

def terms_and_conditions(request):
    return render(request, 'landing/terms.html', get_mock_terms_data())

def shipping_policy(request):
    return render(request, 'landing/shipping.html', get_mock_shipping_policy_data())

def return_policy(request):
    return render(request, 'landing/return.html', get_mock_refund_policy_data())


def payment_methods(request):
    return render(request, 'landing/payment_methods.html', get_mock_payment_methods_data())


def error_404(request, exception):
    return render(request, 'landing/error.html', status=404)
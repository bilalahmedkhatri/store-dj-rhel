from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
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
        
        # Prepare context for the HTML email
        email_context = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message,
        }
        
        # Render the premium HTML email
        html_content = render_to_string('emails/contact_form.html', email_context)
        text_content = strip_tags(html_content)
        
        from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@storedjreheel.com')
        to = ['najeeb.back74@gmail.com']
        
        msg = EmailMultiAlternatives(
            f'Contact Form Inquiry: {subject}',
            text_content,
            from_email,
            to
        )
        msg.attach_alternative(html_content, "text/html")
        
        try:
            msg.send()
        except Exception as e:
            print(f"Error sending contact form email: {e}")
            
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

def complaints(request):
    if request.method == 'POST':
        messages.success(request, 'Your complaint has been registered. Reference ID: CMP-12345. We will get back to you within 48 hours.')
        return redirect('complaints')
    return render(request, 'landing/complaints.html')

def aml_policy(request):
    return render(request, 'landing/aml_policy.html')

def acceptable_use(request):
    return render(request, 'landing/acceptable_use.html')

def merchant_agreement(request):
    return render(request, 'landing/merchant_agreement.html')

def pricing(request):
    return render(request, 'landing/pricing.html')

def kyc(request):
    return render(request, 'landing/kyc.html')

def refund_status(request):
    return render(request, 'landing/refund_status.html')

def security(request):
    return render(request, 'landing/security.html')

def cookie_policy(request):
    return render(request, 'landing/cookie_policy.html')

def status_page(request):
    return render(request, 'landing/status.html')

def contact_email_preview(request):
    mock_context = {
        'name': 'Bilal Ahmed Khatri',
        'email': 'bilal@example.com',
        'subject': 'Inquiry regarding custom embroidery service',
        'message': "Hello Team,\n\nI would love to know if you provide custom sizing or embroidery options for the MukhtaleefWear premium hoodie collection. Specifically, I am interested in ordering 10 units with my startup company logo.\n\nBest regards,\nBilal Khatri",
    }
    return render(request, 'emails/contact_form.html', mock_context)

def error_404(request, exception):
    return render(request, 'landing/error.html', status=404)
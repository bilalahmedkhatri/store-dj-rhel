from django import forms
from django.core import validators
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'fullname', 'streetline1', 
            'city', 'province', 'postalcode', 'phonenumber', 
            'defaultshippingaddress', 'defaultbillingaddress'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We will apply classes in the template for better dynamic control
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'profile-input'})
        
        self.fields['defaultshippingaddress'].label = "Set as default shipping address"
        self.fields['defaultbillingaddress'].label = "Set as default billing address"

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-5 py-3 border border-gray-200 focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all bg-white',
            'placeholder': '••••••••'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Name"
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-5 py-3 border border-gray-200 focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all bg-white',
            'placeholder': 'Enter your full name'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'w-full px-5 py-3 border border-gray-200 focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all bg-white',
            'placeholder': 'Enter your email address'
        })
        
        # Remove default help text and customize error messages
        for field_name in self.fields:
            self.fields[field_name].help_text = ""
            
        if 'username' in self.fields:
            from django.core import validators
            # Allow spaces in the name (username field)
            self.fields['username'].validators = [
                validators.RegexValidator(
                    r'^[\w.@+ \-]+$',
                    'Enter a valid name.',
                    'invalid'
                )
            ]
            self.fields['username'].error_messages['invalid'] = "Please enter a valid name."

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to username field
        self.fields['username'].label = "Email"
        self.fields['username'].widget = forms.EmailInput(attrs={
            'class': 'w-full px-5 py-3 border border-gray-200 focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all',
            'placeholder': 'Enter your email'
        })
        # Add CSS classes to password field

        # Allow spaces in the name (username field)
        self.fields['username'].validators = [
            validators.RegexValidator(
                r'^[\w.@+ \-]+$',
                'Enter a valid name.',
                'invalid'
            )
        ]
        self.fields['username'].error_messages['invalid'] = "Please enter a valid name."
        # Add CSS classes to password field
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-5 py-3 border border-gray-200 focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all',
            'placeholder': '••••••••'
        })
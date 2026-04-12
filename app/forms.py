from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    merchant_type = forms.ChoiceField(
        choices=[('individual', 'Individual'), ('business', 'Registered Business')],
        required=True,
        widget=forms.Select(attrs={'class': 'w-full px-5 py-3 border border-gray-200 rounded-2xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all bg-white'})
    )
    ntn = forms.CharField(
        required=False, 
        label="NTN Number",
        widget=forms.TextInput(attrs={'placeholder': '1234567-8', 'class': 'w-full px-5 py-3 border border-gray-200 rounded-2xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all bg-white'})
    )
    cnic = forms.CharField(
        required=False,
        label="CNIC Number",
        widget=forms.TextInput(attrs={'placeholder': '42101-1234567-1', 'class': 'w-full px-5 py-3 border border-gray-200 rounded-2xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all bg-white'})
    )
    utility_bill = forms.FileField(required=False, label="Utility Bill (Recent)")
    cnic_front = forms.FileField(required=False, label="CNIC Front Side")
    cnic_back = forms.FileField(required=False, label="CNIC Back Side")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to standard fields
        for field_name, field in self.fields.items():
            if field_name in ['username', 'email', 'password1', 'password2']:
                placeholder = ''
                if field_name == 'username': placeholder = 'Enter your username'
                elif field_name == 'email': placeholder = 'Enter your email address'
                elif field_name == 'password1': placeholder = 'Create a password'
                elif field_name == 'password2': placeholder = 'Confirm your password'
                
                field.widget.attrs.update({
                    'class': 'w-full px-5 py-3 border border-gray-200 rounded-2xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all bg-white',
                    'placeholder': placeholder
                })
            
            # File fields styling
            if isinstance(field, forms.FileField):
                field.widget.attrs.update({
                    'class': 'w-full px-5 py-3 border border-gray-200 rounded-2xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all bg-white text-sm'
                })
        
        # Add help text styling
        for field_name in self.fields:
            self.fields[field_name].help_text = None  # Remove default help text

    class Meta:
        model = User
        fields = ("username", "email", "merchant_type", "ntn", "cnic", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            # Logic to save MerchantProfile would go here
        return user


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to username field
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-5 py-3 border border-gray-200 rounded-2xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all',
            'placeholder': 'Enter your username'
        })
        # Add CSS classes to password field
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-5 py-3 border border-gray-200 rounded-2xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all',
            'placeholder': '••••••••'
        })
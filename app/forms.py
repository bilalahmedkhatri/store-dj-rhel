from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to all fields
        for field_name, field in self.fields.items():
            if field_name == 'username':
                field.widget.attrs.update({
                    'class': 'w-full px-5 py-3 border border-gray-200 rounded-2xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all bg-white',
                    'placeholder': 'Enter your username'
                })
            elif field_name == 'email':
                field.widget.attrs.update({
                    'class': 'w-full px-5 py-3 border border-gray-200 rounded-2xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all bg-white',
                    'placeholder': 'Enter your email address'
                })
            elif field_name == 'password1':
                field.widget.attrs.update({
                    'class': 'w-full px-5 py-3 border border-gray-200 rounded-2xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all bg-white',
                    'placeholder': 'Create a password'
                })
            elif field_name == 'password2':
                field.widget.attrs.update({
                    'class': 'w-full px-5 py-3 border border-gray-200 rounded-2xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all bg-white',
                    'placeholder': 'Confirm your password'
                })
        
        # Add help text styling
        for field_name in self.fields:
            self.fields[field_name].help_text = None  # Remove default help text

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
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
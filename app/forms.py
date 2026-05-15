from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-5 py-3 border border-gray-200 rounded-2xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all bg-white',
            'placeholder': '••••••••'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Name"
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-5 py-3 border border-gray-200 rounded-2xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all bg-white',
            'placeholder': 'Enter your full name'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'w-full px-5 py-3 border border-gray-200 rounded-2xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all bg-white',
            'placeholder': 'Enter your email address'
        })
        
        # Remove default help text
        for field_name in self.fields:
            self.fields[field_name].help_text = None

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
        self.fields['username'].label = "Name"
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-5 py-3 border border-gray-200 rounded-2xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all',
            'placeholder': 'Enter your name'
        })
        # Add CSS classes to password field
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-5 py-3 border border-gray-200 rounded-2xl focus:border-primary focus:outline-none focus:ring-4 focus:ring-primary/10 transition-all',
            'placeholder': '••••••••'
        })
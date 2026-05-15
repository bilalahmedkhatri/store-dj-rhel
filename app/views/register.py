from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from ..forms import UserRegistrationForm, CustomAuthenticationForm

def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index') 
        else:
            return render(request, 'landing/register.html', {'register_form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'landing/register.html', {'register_form': form})

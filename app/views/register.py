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
            # If form is invalid, keep the register_form with errors
            login_form = CustomAuthenticationForm()
            return render(request, 'landing/register.html', {
                'register_form': form, 
                'login_form': login_form
            })
    else:
        form = UserRegistrationForm()
        login_form = CustomAuthenticationForm()
    return render(request, 'landing/register.html', {
        'register_form': form, 
        'login_form': login_form
    })

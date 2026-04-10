from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from ..forms import UserRegistrationForm, CustomAuthenticationForm


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            # If form is invalid, keep the login_form with errors
            register_form = UserRegistrationForm()
            return render(request, 'landing/register.html', {
                'login_form': form, 
                'register_form': register_form
            })
    else:
        form = CustomAuthenticationForm()
        register_form = UserRegistrationForm()
    return render(request, 'landing/register.html', {
        'login_form': form, 
        'register_form': register_form
    })

def logout_view(request):
    logout(request)
    return redirect('index')
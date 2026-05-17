from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from ..forms import UserRegistrationForm, CustomAuthenticationForm

def register_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Specify which backend to use for login since we have multiple backends
            login(request, user, backend='app.auth_backends.EmailBackend')
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard') 
        else:
            return render(request, 'landing/register.html', {'register_form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'landing/register.html', {'register_form': form})

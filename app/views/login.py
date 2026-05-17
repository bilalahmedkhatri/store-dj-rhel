from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from ..forms import UserRegistrationForm, CustomAuthenticationForm


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Specify the backend explicitly to avoid ValueError
            login(request, user, backend='app.auth_backends.EmailBackend')
            return redirect('dashboard')
        else:
            return render(request, 'landing/login.html', {'login_form': form})
    else:
        form = CustomAuthenticationForm()
    return render(request, 'landing/login.html', {'login_form': form})

def logout_view(request):
    logout(request)
    return redirect('index')
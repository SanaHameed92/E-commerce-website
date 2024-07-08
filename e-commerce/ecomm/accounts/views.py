from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Account
from .forms import AdminLoginForm
from .forms import SignupForm
from .forms import LoginForm


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            print(f"Email: {email}, Password: {password}")
            
            user = authenticate(request, username=email, password=password)  # Using email for authentication
            
            print(f"Authenticated User: {user}")
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful.')
                return redirect('product_page:shop')  # Ensure the namespace and URL name are correct
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login_page.html', {'form': form})


def admin_login(request):
    if request.method == 'POST':
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user and user.is_active and user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid username or password for admin.')
        else:
            messages.error(request, 'Invalid username or password for admin.')

    form = AdminLoginForm()
    return render(request, 'accounts/admin_login.html', {'form': form})

@login_required
def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, 'accounts/admin_dashboard.html')
    else:
        return redirect('product_page:index')

def logout_view(request):
    auth_logout(request)
    return redirect('main_page:index')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            email = form.cleaned_data.get('email')  # Get the email from the form
            raw_password = form.cleaned_data.get('password')  # Get the raw password from the form
            
            print(f"New User Registered - Email: {email}, Password: {raw_password}")
            
            user = authenticate(username=email, password=raw_password)  # Authenticate the user
            
            print(f"Authenticated User: {user}")
            
            if user is not None:
                login(request, user)  # Log in the user
                messages.success(request, 'Account created successfully. You are now logged in.')
                return redirect('product_page:shop')  # Redirect to the shop page after successful login
            else:
                messages.error(request, 'Account created but unable to log in. Please try logging in manually.')
                return redirect('login')  # Redirect to the login page if unable to log in automatically
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = SignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})



def forgotPassword(request):
    return render(request,'accounts/forgotPassword.html')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product, Category,ProductImage
from products.forms import ProductForm, ProductImageForm
from .forms import AdminLoginForm, SignupForm, LoginForm,CategoryForm 
from django.contrib.auth import get_user_model
from django.conf import settings
from .forms import CustomPasswordResetForm, OTPVerificationForm, CustomSetPasswordForm
from .utils import generate_otp,send_otp_email
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator



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
                messages.success(request, 'Account created successfully. You can now log In.')
                return redirect('login')  # Redirect to the shop page after successful login
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

def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, 'accounts/admin_dashboard.html')
    else:
        return redirect('product_page:index')

def admin_products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added successfully.')
            return redirect('admin_products')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CategoryForm()

    return render(request, 'admin_side/admin_products.html', {
        'products': products,
        'categories': categories,
        'form': form
    })

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        image_form = ProductImageForm(request.POST, request.FILES)
        
        if form.is_valid():
            product_instance = form.save(commit=False)
            product_instance.updated_by = request.user  # Assuming you have an updated_by field
            product_instance.save()

            if image_form.is_valid():
                for image in request.FILES.getlist('additional_images'):
                    ProductImage.objects.create(product=product_instance, image=image)

            messages.success(request, 'Product updated successfully.')
            return redirect('admin_products')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)
        image_form = ProductImageForm()

    return render(request, 'admin_side/edit_product.html', {'form': form, 'product': product, 'categories': categories, 'image_form': image_form})





def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('admin_products')  # Redirect to the product list page or wherever appropriate

    return render(request, 'admin_side/confirm_delete_product.html', {'product': product})


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully.')
        return redirect('admin_products')
    
    return render(request, 'admin_side/confirm_delete_category.html', {'category': category})

def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        image_form = ProductImageForm(request.POST, request.FILES)
        if product_form.is_valid() and image_form.is_valid():
            product = product_form.save(commit=False)
            product.created_by = request.user  # Assuming you have implemented user authentication
            product.save()
            image = image_form.save(commit=False)
            image.product = product
            image.save()
            return redirect('admin_products')  # Redirect to admin products list after adding
    else:
        product_form = ProductForm()
        image_form = ProductImageForm()

    return render(request, 'admin_side/add_products.html', {'product_form': product_form, 'image_form': image_form})







UserModel = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = UserModel.objects.get(email=email)
                otp = generate_otp()
                user.otp = otp
                user.save()
                send_otp_email(email, otp)
                messages.success(request, 'OTP has been sent to your email address.')
                return redirect('verify_otp')
            except UserModel.DoesNotExist:
                messages.error(request, 'No account found with this email address.')
    else:
        form = CustomPasswordResetForm()

    return render(request, 'accounts/forgot_password.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_entered = form.cleaned_data['otp']
            try:
                user = UserModel.objects.get(otp=otp_entered)
                user.otp = None
                user.save()
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                return redirect('password_reset_confirm', uidb64=uid, token=token)
            except UserModel.DoesNotExist:
                messages.error(request, "Invalid OTP entered.")
    else:
        form = OTPVerificationForm()

    return render(request, 'accounts/verify_otp.html', {'form': form})


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('login')
    form_class = CustomSetPasswordForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uidb64'] = self.kwargs['uidb64']
        context['token'] = self.kwargs['token']
        return context
    

   


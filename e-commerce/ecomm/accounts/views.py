from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Brand, Color, Order, Product, Category,ProductImage, Size
from products.forms import BrandForm, CategoryForm, ColorForm, ProductForm, ProductImageForm, SizeForm
from .forms import AdminLoginForm, SignupForm, LoginForm
from django.contrib.auth import get_user_model
from django.conf import settings
from .forms import CustomPasswordResetForm, OTPVerificationForm, CustomSetPasswordForm
from .utils import generate_otp,send_otp_email
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetConfirmView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import Account



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

                if user.is_active:
                    login(request, user)
                    return redirect('product_page:shop')  # Redirect to your desired page
                else:
                    messages.error(request, 'Account is inactive.',extra_tags='login')
            else:
                messages.error(request, 'Invalid email or password.',extra_tags='login')
        else:
            messages.error(request, 'Please correct the errors below.',extra_tags='login')
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
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Ensure password is hashed
            user.is_active = False
            user.otp = generate_otp() 
            user.save()
              # Save the user

            send_otp_email(user.email, user.otp)
           
            messages.success(request, 'OTP has been sent to your email address. Please verify.', extra_tags='otp')
            return redirect('verify_otp', user_id=user.pk, scenario='signup')  # Redirect to the shop page after successful login
            #else:
                #messages.error(request, 'Account created but unable to log in. Please try logging in manually.')
                #return redirect('login')  # Redirect to the login page if unable to log in automatically
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field.capitalize()}: {error}')
    else:
        form = SignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def admin_dashboard(request):
    orders = Order.objects.all()
    if request.user.is_authenticated and request.user.is_staff:
        return render(request, 'accounts/admin_dashboard.html', {'orders': orders})
    else:
        return redirect('product_page:index')

def admin_products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()
    sizes = Size.objects.all()
    colors = Color.objects.all()

    if request.method == 'POST':
        category_form = CategoryForm(request.POST)
        brand_form = BrandForm(request.POST)
        size_form = SizeForm(request.POST)
        color_form = ColorForm(request.POST)

        if category_form.is_valid():
            category_form.save()
            messages.success(request, 'Category added successfully.', extra_tags='product_update')
            return redirect('admin_products')
        elif brand_form.is_valid():
            brand_form.save()
            messages.success(request, 'Brand added successfully.', extra_tags='product_update')
            return redirect('admin_products')
        elif size_form.is_valid():
            size_form.save()
            messages.success(request, 'Size added successfully.')
            return redirect('admin_products')
        elif color_form.is_valid():
            color_form.save()
            messages.success(request, 'Color added successfully.')
            return redirect('admin_products')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        category_form = CategoryForm()
        brand_form = BrandForm()
        size_form = SizeForm()
        color_form = ColorForm()

    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
        'sizes': sizes,
        'colors': colors,
        'category_form': category_form,
        'brand_form': brand_form,
        'size_form': size_form,
        'color_form': color_form,
    }
    return render(request, 'admin_side/admin_products.html', context)

def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()

    existing_images = product.images.all()
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        image_form = ProductImageForm(request.POST, request.FILES)
        
        
        if form.is_valid():
            product_instance = form.save(commit=False)
            product_instance.updated_by = request.user  # Assuming you have an updated_by field
            product.sizes.set(form.cleaned_data['sizes'])
            product.colors.set(form.cleaned_data['colors'])
          
            product_instance.save()

            for image in existing_images:
                image_field_name = f'image_{image.id}'
                if image_field_name in request.FILES:
                    image.image = request.FILES[image_field_name]
                    image.save()

            messages.success(request, 'Product updated successfully.', extra_tags='product_update')
            return redirect('admin_products')
        else:
            messages.error(request, 'Please correct the errors below.', extra_tags='product_update')
    else:
        form = ProductForm(instance=product)
        image_form = ProductImageForm()

    return render(request, 'admin_side/edit_product.html', {
        'form': form, 
        'product': product, 
        'categories': categories, 
        'image_form': image_form,
        'existing_images': existing_images})





def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        # Update availability status instead of deleting
        if product.availability_status == 'in_stock':
            product.availability_status = 'out_of_stock'
        else:
            product.availability_status = 'in_stock'
        product.save()
        
        messages.success(request, f'Availability of "{product.title}" changed successfully.', extra_tags='product_update')
        return redirect('admin_products')  # Redirect to the product list page or wherever appropriate
    
    return render(request, 'admin_side/confirm_delete_product.html', {'product': product})


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        # Toggle is_active status instead of deleting
        category.is_active = not category.is_active  # Assuming 'is_active' is a BooleanField
        category.save()
        
        messages.success(request, 'Category status changed successfully.', extra_tags='product_update')
        return redirect('admin_products')  # Redirect to the admin products page or appropriate view
    
    return render(request, 'admin_side/confirm_delete_category.html', {'category': category})

def toggle_brand_status(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    brand.is_active = not brand.is_active  # Toggle the status
    brand.save()
    return redirect('admin_products')

def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)

        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.created_by = request.user
            product.save()
            product_form.save_m2m()

            # Handle main product image
            main_image = request.FILES.get('product_image')
            if main_image:
                ProductImage.objects.create(product=product, image=main_image, is_main=True)

            # Handle additional images
            additional_images = request.FILES.getlist('additional_images')
            for image in additional_images:
                ProductImage.objects.create(product=product, image=image, is_main=False)

            return redirect('admin_products')

    else:
        product_form = ProductForm()

    return render(request, 'admin_side/add_products.html', {'product_form': product_form})


UserModel = get_user_model()

def forgot_password(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                #user = UserModel.objects.get(email=email)
                user = Account.objects.get(email=email)
                otp = generate_otp()
                user.otp = otp
                user.save()

                #send_otp_email(email, otp)
                send_otp_email(user.email, user.otp)
                messages.success(request, 'OTP has been sent to your email address.', extra_tags='otp')
                return redirect('verify_otp', user.pk, 'forgot_password')
            #except UserModel.DoesNotExist:
            except Account.DoesNotExist:
                messages.error(request, 'No account found with this email address.', extra_tags='otp')
    else:
        form = CustomPasswordResetForm()

    return render(request, 'accounts/forgot_password.html', {'form': form})

def verify_otp(request, user_id, scenario):
    try:
        user = UserModel.objects.get(pk=user_id)    
    except UserModel.DoesNotExist:
        messages.error(request, "Invalid user.")
        return redirect('login')
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            otp_entered = form.cleaned_data['otp']
            if user.otp == otp_entered:
                user.otp = None
                user.is_active = True
                user.save()
                if scenario == 'signup':
                    user.backend = 'django.contrib.auth.backends.ModelBackend'  # Set the authentication backend
                    auth_login(request, user)
                    messages.success(request, 'OTP verified successfully. Now you can log in.')
                    return redirect('login')
                elif scenario == 'forgot_password':
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    token = default_token_generator.make_token(user)
                    return redirect('password_reset_confirm', uidb64=uid, token=token)
            else:
                messages.error(request, "Invalid OTP entered.")
                #user = Account.objects.get(otp=otp_entered)
                #user.backend = 'django.contrib.auth.backends.ModelBackend'
                #login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                #uid = urlsafe_base64_encode(force_bytes(user.pk))
                #token = default_token_generator.make_token(user)
                #login(request, user)
                #messages.success(request, 'OTP verified successfully. You are now logged in.')
                #return redirect('password_reset_confirm', uidb64=uid, token=token)
               
    else:
        form = OTPVerificationForm(initial={'scenario': scenario})

    return render(request, 'accounts/verify_otp.html', {'form': form, 'user': user, 'scenario': scenario})


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    success_url = reverse_lazy('login')
    form_class = CustomSetPasswordForm


    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Password changed successfully. Now you can log in.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uidb64'] = self.kwargs['uidb64']
        context['token'] = self.kwargs['token']
        return context
    

   


from uuid import uuid4
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Address
from .forms import AddressForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from products.models import Order
from django.views.decorators.http import require_POST

User = get_user_model()

@login_required
def personal_information(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')

        # Retrieve the current user instance
        user = request.user

        # Update the user instance with new data
        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number

        # Save the updated user instance
        user.save()

        # Optionally, show a success message
        messages.success(request, 'Your personal information has been updated.')

        # Redirect back to the personal information page or any other desired page
        return redirect('personal_information')

    # If it's a GET request, render the personal information form page
    return render(request, 'user/profile.html')

# Create your views here.
def profile(request):
    user = request.user
    return render(request, 'user/profile.html',{'user':user})

def manage_address(request):
    # Ensure user is authenticated
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated

    # Filter addresses for the logged-in user
    addresses = Address.objects.filter(user=request.user)

    return render(request, 'user/manage_address.html', {'addresses': addresses})

def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user  # Assign the current user
            form.save()
            messages.success(request, 'Address added successfully!')
            return redirect('manage_address')
    else:
        form = AddressForm()
    
    return render(request, 'user/add_address.html', {'form': form})

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('manage_address')
    else:
        form = AddressForm(instance=address)
    
    return render(request, 'user/edit_address.html', {'form': form})

@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)
    if request.method == 'POST':
        address.delete()
        return redirect('manage_address')
    
    return render(request, 'user/delete_address.html', {'address': address})

def reset_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            new_password1 = form.cleaned_data['new_password1']
            new_password2 = form.cleaned_data['new_password2']
            if new_password1 == new_password2:
                user = form.save()
                update_session_auth_hash(request, user)  # Important to update the session
                messages.success(request, 'Your password was successfully updated!')
                return redirect('personal_information')  # Redirect to profile page
            else:
                messages.error(request, "Passwords do not match. Please enter matching passwords.")
        else:
            messages.error(request, 'Please enter correct password.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'user/profile.html', {'form': form})

def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'user/my_orders.html', {'orders': orders})
    


def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    return render(request, 'user/order_detail.html', {'order': order})


def cancel_order(request, order_number):
    # Fetch the order for the current user
    
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    # Check if the order is not already cancelled
    if order.status != 'Cancelled':
        # Update the status to 'Cancelled'
        order.status = 'Cancelled'
        
        # Restore product quantities
        for item in order.items.all():
            product = item.product
            product.quantity += item.quantity
            product.save()
        
        # Save the updated order status
        order.save()

        # Display a success message
        messages.success(request, "Order cancelled successfully!")
    else:
        # If the order is already cancelled, display an info message
        messages.info(request, "Order is already cancelled.")
    
    # Redirect to the order detail or any other page you prefer
    return redirect('order_detail', order_number=order_number)


def order_list(request):
    orders = Order.objects.all().order_by('-created_at')  # Adjust according to your model and filtering needs
    return render(request, 'admin_side/order_list.html', {'orders': orders})

@require_POST
def update_order_status(request):
    order_id = request.POST.get('order_id')
    new_status = request.POST.get('status')
    order = Order.objects.get(id=order_id)
    order.status = new_status
    order.save()
    return redirect('order_list')
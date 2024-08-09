from datetime import datetime, timedelta
from django.utils import timezone
import uuid
from django.shortcuts import render, get_object_or_404
from .models import Cart, CartItem, Coupon, Order, OrderItem, Product, Category, Brand, ProductVariant, Size, Color
from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from User.models import Address
from django.db.models import Count
from .forms import CouponForm, ProductVariantForm
import razorpay



def shop(request):
    category_name = request.GET.get('category')
    brand_name = request.GET.get('brand')
    color = request.GET.get('color')
    sort = request.GET.get('sort')
    size = request.GET.get('size')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    cart_items_count = CartItem.objects.filter(cart__user=request.user).count()

    product_list = Product.objects.all()

    # Apply category filter
    if category_name:
        product_list = product_list.filter(category__category_name=category_name)

    # Apply brand filter
    if brand_name:
        product_list = product_list.filter(brand__brand_name=brand_name)

    # Apply color filter
    if color:
        product_list = product_list.filter(colors__color_name=color)

    # Apply size filter
    if size:
        try:
            selected_size = Size.objects.get(size_name=size)
            product_list = product_list.filter(sizes=selected_size)
        except Size.DoesNotExist:
            pass

    # Apply price range filter
    if min_price:
        try:
            min_price = float(min_price)
            product_list = product_list.filter(original_price__gte=min_price)
        except ValueError:
            pass
    if max_price:
        try:
            max_price = float(max_price)
            product_list = product_list.filter(original_price__lte=max_price)
        except ValueError:
            pass

    # Annotate products with purchase counts
    product_list = product_list.annotate(cart_count=Count('cartitem'))

    # Apply sorting
    if sort == 'popularity':
        product_list = product_list.order_by('-cart_count')
    elif sort == 'price_low_high':
        product_list = product_list.order_by('original_price')
    elif sort == 'price_high_low':
        product_list = product_list.order_by('-original_price')
    elif sort == 'average_ratings':
        product_list = product_list.order_by('-rating')
    elif sort == 'featured':
        product_list = product_list.order_by('-featured')
    elif sort == 'new_arrivals':
        product_list = product_list.order_by('-created_at')
    elif sort == 'a_z':
        product_list = product_list.order_by('title')
    elif sort == 'z_a':
        product_list = product_list.order_by('-title')
    else:
        product_list = product_list.order_by('-created_at')

    # Paginate the product list
    product_paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page')
    product_list = product_paginator.get_page(page_number)

    # Fetch categories, brands, sizes, and colors
    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(is_active=True)
    sizes = Size.objects.all()
    colors = Color.objects.all()

    context = {
        'products': product_list,
        'categories': categories,
        'brands': brands,
        'sizes': sizes,
        'colors': colors,
        'selected_category': category_name,
        'selected_brand': brand_name,
        'selected_color': color,
        'selected_size': size,
        'selected_sort': sort,
        'min_price': min_price,
        'max_price': max_price,
        'cart_items_count': cart_items_count,
        'product_error': request.session.pop('product_error', None)
    }

    return render(request, 'shop.html', context)



def shop_single(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    features_products = Product.objects.filter(trending=True)[:3]

    # Get sizes and colors for the product
    sizes = product.sizes.all()
    colors = product.colors.all()

    # Display error message if any
    product_error = messages.get_messages(request)
    for message in product_error:
        if 'shop-single' in message.tags:
            messages.error(request, message.message)

    context = {
        'product': product,
        'featured_items': features_products,
        'sizes': sizes,
        'colors': colors,
        'availability_message': "Only 1 item left" if product.quantity == 1 else "",
    }
    return render(request, 'shop-single.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get the quantity, size, and color from the POST request
    quantity = int(request.POST.get('quantity', 1))
    size_id = request.POST.get('size')
    color_id = request.POST.get('color')
    
    # Retrieve size and color if provided
    size = Size.objects.get(id=size_id) if size_id else None
    color = Color.objects.get(id=color_id) if color_id else None
    
    # Check if there is enough stock available
    if quantity > product.quantity:
        messages.error(request, 'Not enough stock available.')
        return redirect('product_page:shop-single', product_id=product.id)
    
    # Check if the cart item already exists
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, product=product, size=size, color=color
    )
    
    if not item_created:
        if cart_item.quantity + quantity > product.quantity:
            messages.error(request, 'Not enough stock available to add this quantity.')
            return redirect('product_page:shop-single', product_id=product.id)
        
        if cart_item.quantity + quantity > product.max_qty_per_person:
            messages.error(request, f'You can only add up to {product.max_qty_per_person} items of this product.')
            return redirect('product_page:shop-single', product_id=product.id)
        
        cart_item.quantity += quantity
        cart_item.save()
    else:
        if quantity > product.max_qty_per_person:
            messages.error(request, f'You can only add up to {product.max_qty_per_person} items of this product.')
            return redirect('product_page:shop-single', product_id=product.id)
        
        cart_item.quantity = quantity
        cart_item.save()
    
    referrer = request.META.get('HTTP_REFERER', '')
    if 'shop-single' in referrer:
        return redirect('product_page:cart')
    
    return redirect('product_page:shop')

def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_items_count = cart_items.count()
    
    # Retrieve any product error message from the session
    product_error = request.session.pop('product_error', None)
    
    context = {
        'cart_items': cart_items,
        'total': sum(item.total_price for item in cart_items),
        'cart_items_count': cart_items_count,
        'product_error': product_error
    }
    
    return render(request, 'cart.html', context)

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
   
    return redirect('product_page:cart')




def product_filter_by_size(request):
    size = request.GET.get('size')
    products = Product.objects.filter(sizes__size_name=size)
    small_count = Product.objects.filter(sizes__size_name='Small').count()
    medium_count = Product.objects.filter(sizes__size_name='Medium').count()
    large_count = Product.objects.filter(sizes__size_name='Large').count()
    context = {
        'products': products,
        'selected_size': size,  
        'small_count': small_count,
        'medium_count': medium_count,
        'large_count': large_count,
        }
    
    return render(request, 'shop.html', context)

def product_filter_by_color(request):
    color = request.GET.get('color')
    products = Product.objects.filter(colors__color_name=color)
    context = {'products': products}
    return render(request, 'shop.html', context)


def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate total and shipping fee
    total = sum(item.total_price for item in cart_items)
    shipping_fee = 50 if total <= 350 else 0

    # Initialize variables for coupon code processing
    coupon_code = request.POST.get('coupon_code', '').strip()
    discount = 0
    message = "Coupon code applied successfully."
    success = True
    applied_coupon_code = None

    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            coupon.update_status()  # Make sure this method updates coupon status
            if coupon.status == 'active':
                discount = coupon.discount
                applied_coupon_code = coupon_code
            else:
                message = "Invalid or expired coupon code."
                success = False
        except Coupon.DoesNotExist:
            message = "Coupon code does not exist."
            success = False

    # Calculate the discount amount based on the percentage
    discount_amount = (total * discount / 100)
    grand_total = total + shipping_fee - discount_amount

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        response_data = {
            'success': success,
            'message': message,
            'new_total': grand_total,  # Ensure this is a number
            'applied_coupon_code': applied_coupon_code,
            'discount': discount
        }
        return JsonResponse(response_data)
    
    # Calculate estimated delivery date
    delivery_days = 5
    estimated_delivery_date = timezone.now() + timedelta(days=delivery_days)
    formatted_delivery_date = estimated_delivery_date.strftime('%d %b %Y')

    # Retrieve addresses for the user
    addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-created_at')

    if request.method == 'POST':
        address_id = request.POST.get('selected_address')
        payment_method = request.POST.get('payment_method')

        # Validate address and payment method
        if not address_id:
            messages.error(request, "Please select a shipping address.")
            return redirect('product_page:checkout')

        if not payment_method:
            messages.error(request, "Please select a payment method.")
            return redirect('product_page:checkout')

        try:
            selected_address = Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            messages.error(request, "Selected address does not exist.")
            return redirect('product_page:checkout')

        formatted_address = (f"{selected_address.first_name} {selected_address.last_name}, "
                              f"{selected_address.street_address}, {selected_address.city}, "
                              f"{selected_address.state}, {selected_address.country}, "
                              f"{selected_address.postal_code}")

        # Store data in session
        cart_items_data = [
            {
                'title': item.product.title,
                'quantity': item.quantity,
                'total_price': float(item.total_price)
            } for item in cart_items
        ]
        request.session['cart_items'] = cart_items_data
        request.session['total'] = float(total)
        request.session['shipping_fee'] = float(shipping_fee)
        request.session['grand_total'] = float(grand_total)
        request.session['selected_address'] = {
            'address': formatted_address,
            'id': selected_address.id,
            'payment_method': payment_method,
        }
        request.session['estimated_delivery_date'] = formatted_delivery_date

        # Redirect based on payment method
        if payment_method == 'RazorPay':
            return redirect('product_page:razorpaycheck')
        elif payment_method == 'COD':
            return redirect('product_page:order_summary')
        else:
            messages.error(request, "Invalid payment method selected.")
            return redirect('product_page:checkout')

    context = {
        'cart_items': cart_items,
        'total': total,
        'shipping_fee': shipping_fee,
        'grand_total': grand_total,
        'addresses': addresses,
        'formatted_delivery_date': formatted_delivery_date,
    }

    return render(request, 'user/checkout.html', context)


def order_summary(request):
    cart_items = request.session.get('cart_items', [])
    total = request.session.get('total', 0)
    shipping_fee = request.session.get('shipping_fee', 0)
    grand_total = request.session.get('grand_total', 0)
    selected_address = request.session.get('selected_address', {})

    # Extract address details
    formatted_address = selected_address.get('address', 'No address selected')
    payment_method = selected_address.get('payment_method', 'Not Provided')
    

    context = {
        'cart_items': cart_items,
        'total': total,
        'shipping_fee': shipping_fee,
        'grand_total': grand_total,
        'formatted_address': formatted_address,
        'payment_method': payment_method,
    }

    return render(request, 'user/order_summary.html', context)


def update_cart(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 0))

        try:
            cart = Cart.objects.get(user=request.user)
            item = CartItem.objects.get(cart=cart, id=item_id)
            product = item.product

            # Check if quantity exceeds stock
            if quantity > product.quantity:
                return JsonResponse({'success': False, 'error_message': f"Not enough stock available for {product.title}."})
            # Check if quantity exceeds maximum allowed per person
            elif quantity > product.max_qty_per_person:
                return JsonResponse({'success': False, 'error_message': f"Quantity exceeds limit for {product.title}."})
            else:
                item.quantity = quantity
                item.save()
                return JsonResponse({'success': True})

        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Cart not found.'})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error_message': 'Cart item not found.'})
        except ValueError:
            return JsonResponse({'success': False, 'error_message': 'Invalid quantity.'})

    return JsonResponse({'success': False, 'error_message': 'Invalid request method'}, status=405)


def place_order(request):
    if request.method == 'POST':
        cart_items_data = request.session.get('cart_items', [])
        total = request.session.get('total', 0)
        shipping_fee = request.session.get('shipping_fee', 0)
        grand_total = request.session.get('grand_total', 0)
        selected_address = request.session.get('selected_address', {})
        address_id = selected_address.get('id')
        payment_method = selected_address.get('payment_method')
        payment_id = request.POST.get('payment_id')

        if not cart_items_data or not address_id:
            return JsonResponse({'status': "Incomplete order details"}, status=400)

        try:
            selected_address = Address.objects.get(id=address_id)

            for item_data in cart_items_data:
                if item_data['quantity'] <= 0:
                    return JsonResponse({'status': f"Invalid quantity for product {item_data['title']}."}, status=400)

            order = Order.objects.create(
                user=request.user,
                address=selected_address,
                payment_method=payment_method,
                total_amount=total,
                shipping_fee=shipping_fee,
                grand_total=grand_total,
                order_number=str(uuid.uuid4()),
                status='Ordered',
                payment_id=payment_id,
            )

            for item_data in cart_items_data:
                product = Product.objects.get(title=item_data['title'])

                if product.quantity < item_data['quantity']:
                    return JsonResponse({'status': f"Insufficient stock for product {product.title}."}, status=400)

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item_data['quantity'],
                    total_price=item_data['total_price']
                )

                product.quantity -= item_data['quantity']
                product.popularity += item_data['quantity']
                product.save()

            CartItem.objects.filter(cart__user=request.user).delete()

            return redirect('product_page:order_success', order_number=order.order_number)

        except Exception as e:
            return JsonResponse({'status': f"An error occurred while placing the order: {e}"}, status=500)



def order_success(request, order_number):
    
    # Fetch the order using the order_number
    order = get_object_or_404(Order, order_number=order_number)
    
    context = {
        'order': order,
        'order_number': order_number,
      
    }

    return render(request, 'user/order_success.html', context)





def coupon_list(request):
    coupons = Coupon.objects.all()
    return render(request, 'admin_side/coupon_list.html', {'coupons': coupons})

def coupon_add(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_page:coupon_list')
    else:
        form = CouponForm()
    return render(request, 'admin_side/coupon_form.html', {'form': form})

def coupon_edit(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == 'POST':
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            return redirect('product_page:coupon_list')
    else:
        form = CouponForm(instance=coupon)
    return render(request, 'admin_side/coupon_form.html', {'form': form})

def coupon_delete(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)

    # Directly update the status field
    if coupon.status == 'active':
        coupon.status = 'inactive'
    else:
        coupon.status = 'active'
    
    coupon.save(update_fields=['status'])  # Use update_fields to only save the status field

    return redirect('product_page:coupon_list')


def list_product_variants(request):
    variants = ProductVariant.objects.all()
    return render(request, 'admin_side/product_variants.html', {'variants': variants})

def add_product_variant(request):
    if request.method == 'POST':
        form = ProductVariantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('product_page:list_product_variants'))
    else:
        form = ProductVariantForm()
    return render(request, 'admin_side/product_variants_form.html', {'form': form})

def edit_product_variant(request, pk):
    variant = get_object_or_404(ProductVariant, pk=pk)
    if request.method == 'POST':
        form = ProductVariantForm(request.POST, instance=variant)
        if form.is_valid():
            form.save()
            return redirect(reverse('product_page:list_product_variants'))
    else:
        form = ProductVariantForm(instance=variant)
    return render(request, 'admin_side/product_variants_form.html', {'form': form})

def delete_product_variant(request, pk):
    variant = get_object_or_404(ProductVariant, pk=pk)
    if request.method == 'POST':
        variant.delete()
        return redirect(reverse('product_page:list_product_variants'))
    return render(request, 'confirm_delete.html', {'object': variant})


def razorpaycheck(request):
    cart = Cart.objects.filter(user=request.user).first()
    total_price = sum(item.total_price for item in CartItem.objects.filter(cart=cart))
    shipping_fee = 50 if total_price <= 350 else 0  # Example shipping fee, replace with your actual logic
    grand_total = total_price + shipping_fee
    
    
    # You can decide on how to get the address_id, for simplicity, I'm using the first address
    address = Address.objects.filter(user=request.user).first()
    
    
    if not address:
        return JsonResponse({'error': 'No address found for the user'}, status=400)
    
    # Create a preliminary order with status 'Pending'
    order = Order.objects.create(
        user=request.user,
        address=address,
        payment_method='RazorPay',  # Since it's a razorpaycheck
        total_amount=total_price,
        shipping_fee=shipping_fee,
        grand_total=grand_total,
        order_number=str(uuid.uuid4()),
        status='Pending',
    )
    
    return JsonResponse({
        'total_price': grand_total,
        'first_name': request.user.first_name,
        'email': request.user.email,
        'phone_number': request.user.phone_number,
        'order_id': order.order_number,  # Include order_id in the response
    })

def confirm_order_razorpay(request):
    if request.method == 'POST':
        order_number = request.POST.get('order_id')
        payment_id = request.POST.get('payment_id')
        
        try:
            order = Order.objects.get(order_number=order_number)
            order.payment_id = payment_id
            order.status = 'Ordered'
            order.save()
            
            cart_items = CartItem.objects.filter(cart__user=request.user)
            for cart_item in cart_items:
                product = cart_item.product
                
                if product.quantity < cart_item.quantity:
                    return JsonResponse({'status': f"Insufficient stock for product {product.title}."}, status=400)
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=cart_item.quantity,
                    total_price=cart_item.total_price,
                )
                
                product.quantity -= cart_item.quantity
                product.popularity += cart_item.quantity
                product.save()
            
            CartItem.objects.filter(cart__user=request.user).delete()
            
            return JsonResponse({'status': 'Order placed successfully', 'order_number': order.order_number})
        
        except Order.DoesNotExist:
            return JsonResponse({'status': 'Invalid order ID'}, status=400)
        except Exception as e:
            return JsonResponse({'status': f"An error occurred while placing the order: {e}"}, status=500)
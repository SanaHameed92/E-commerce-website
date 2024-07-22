import uuid
from django.shortcuts import render, get_object_or_404
from .models import Cart, CartItem, Order, OrderItem, Product, Category, Brand, Size, Color
from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib import messages
from User.models import Address
from User.forms import AddressForm


def shop(request):
    category_name = request.GET.get('category')
    brand_name = request.GET.get('brand')
    color = request.GET.get('color')
    sort = request.GET.get('sort')
    size = request.GET.get('size')
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
            product_list = product_list.filter(sizes__in=[selected_size])
        except Size.DoesNotExist:
            pass

    if sort == 'popularity':
        product_list = product_list.order_by('-popularity')  # Assuming you have a popularity field
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

    product_paginator = Paginator(product_list, 6)
    page_number = request.GET.get('page')
    product_list = product_paginator.get_page(page_number)

    categories = Category.objects.filter(is_active=True)
    brands = Brand.objects.filter(category__category_name=category_name) if category_name else Brand.objects.none()

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
        'cart_items_count': cart_items_count,
        'product_error': request.session.pop('product_error', None)
    }
   
    return render(request, 'shop.html', context)



def shop_single(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    features_products = Product.objects.filter(trending=True)[:3]
    

    context = {
        'product': product,
        'featured_items': features_products,
        'product_error': request.session.pop('product_error', None),
        'availability_message': "Only 1 item left" if product.quantity == 1 else ""
    }
    return render(request, 'shop-single.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get the quantity from the POST request
    quantity = int(request.POST.get('quantity', 1))
    
    # Check if there is enough stock available
    if product.quantity < quantity:
        messages.error(request, 'Not enough stock available.')
        return redirect('product_page:shop-single', product_id=product.id)
    
    # Check if the cart item already exists
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        if cart_item.quantity + quantity > product.quantity:
            request.session['product_error'] = {
                'product_id': product_id,
                'message': 'Maximum stock limit reached for this product.'
            }
            return redirect('product_page:shop-single', product_id=product.id)
        
        if cart_item.quantity + quantity > product.max_qty_per_person:
            request.session['product_error'] = {
                'product_id': product_id,
                'message': f'You can only add up to {product.max_qty_per_person} items of this product.'
            }
            return redirect('product_page:shop-single', product_id=product.id)
        
        cart_item.quantity += quantity
        cart_item.save()
    else:
        cart_item.quantity = quantity
        cart_item.save()

    messages.success(request, 'Product added to cart!')

    referrer = request.META.get('HTTP_REFERER', '')

    if 'shop-single' in referrer:
        return redirect('product_page:cart')

    return redirect('product_page:shop')


def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_items_count = cart_items.count()
    
    context = {
        'cart_items': cart_items,
        'total': sum(item.total_price for item in cart_items),
        'cart_items_count': cart_items_count,
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
    # Get or create the cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    # Calculate totals and fees
    total = sum(item.total_price for item in cart_items)
    shipping_fee = 50 if total >= 350 else 0
    grand_total = total + shipping_fee

    # Get user's addresses
    addresses = Address.objects.filter(user=request.user)

    if request.method == 'POST':
        address_id = request.POST.get('selected_address')
        payment_method = request.POST.get('payment_method')
        order_notes = request.POST.get('order_notes')

        if address_id:
            try:
                # Fetch the selected address
                selected_address = Address.objects.get(id=address_id)
            except Address.DoesNotExist:
                messages.error(request, "Selected address does not exist.")
                return redirect('checkout')

            # Format address
            formatted_address = (f"{selected_address.first_name} {selected_address.last_name}, "
                                  f"{selected_address.street_address}, {selected_address.city}, "
                                  f"{selected_address.state}, {selected_address.country}, "
                                  f"{selected_address.postal_code}")

            # Prepare data for session
            cart_items_data = [
                {
                    'title': item.product.title,
                    'quantity': item.quantity,
                    'total_price': float(item.total_price)  # Convert to float for JSON serialization
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
            request.session.modified = True

            return redirect('product_page:order_summary')
        else:
            messages.error(request, "Please select a shipping address.")
            return redirect('checkout')

    context = {
        'cart_items': cart_items,
        'total': total,
        'addresses': addresses,
        'grand_total': grand_total,
        'shipping_fee': shipping_fee,
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
        cart_items = CartItem.objects.filter(cart__user=request.user)
        has_error = False
        error_messages = {}

        for item in cart_items:
            quantity = request.POST.get(f'quantity_{item.id}', 0)
            try:
                quantity = int(quantity)
            except ValueError:
                quantity = 0
            
            if quantity <= 0:
                item.delete()
            else:
                if quantity <= item.product.max_qty_per_person:
                    item.quantity = quantity
                    item.save()
                else:
                    error_messages[item.id] = f"Quantity exceeds limit for {item.product.title}."
                    has_error = True
        
        if has_error:
            request.session['error_messages'] = error_messages
            return redirect('product_page:cart')  # Redirect back to cart to display error messages

        # Clear error messages after successful update
        if 'error_messages' in request.session:
            del request.session['error_messages']
        
        return redirect('product_page:cart')  # Redirect back to cart or appropriate page

    return HttpResponse("Invalid request method", status=405)


def place_order(request):
    # Retrieve session data
    cart_items_data = request.session.get('cart_items')
    total = request.session.get('total')
    shipping_fee = request.session.get('shipping_fee')
    grand_total = request.session.get('grand_total')
    #selected_address = request.session.get('selected_address')
    address_id = request.session.get('selected_address', {}).get('id')
    payment_method = request.session.get('selected_address', {}).get('payment_method')

    if not cart_items_data or not address_id:
        messages.error(request, "Incomplete order details.")
        return redirect('product_page:checkout')
    try:

        selected_address = Address.objects.get(id=address_id)
        # Create an Order
        order = Order.objects.create(
            user=request.user,
            address=selected_address,  # Store address as a string
            payment_method=payment_method,
            order_notes=request.POST.get('order_notes', ''),
            total_amount=total,
            shipping_fee=shipping_fee,
            grand_total=grand_total,
            order_number=str(uuid.uuid4())  # Generate a unique order number
        )

        # Create Order Items
        for item_data in cart_items_data:
            product = Product.objects.get(title=item_data['title'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item_data['quantity'],
                total_price=item_data['total_price']
            )

            product.quantity -= item_data['quantity']
            product.save()

        # Clear the cart after placing the order
        CartItem.objects.filter(cart__user=request.user).delete()
        
        # Redirect to order success page with the order number
        return redirect('product_page:order_success', order_number=order.order_number)

    except Exception as e:
        messages.error(request, f"An error occurred while placing the order: {e}")
        return redirect('product_page:checkout')



def order_success(request, order_number):
    # Fetch the order using the order_number
    order = get_object_or_404(Order, order_number=order_number)
    
    context = {
        'order': order,
        'order_number': order_number,
    }

    return render(request, 'user/order_success.html', context)
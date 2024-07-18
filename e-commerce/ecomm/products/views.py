from django.shortcuts import render, get_object_or_404
from .models import Cart, CartItem, Product, Category, Brand, Size, Color
from django.core.paginator import Paginator
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib import messages

def shop(request):
    category_name = request.GET.get('category')
    brand_name = request.GET.get('brand')
    color = request.GET.get('color')
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
        'product_error': request.session.pop('product_error', None)
    }
    return render(request, 'shop-single.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if there is enough stock available
    if product.quantity <= 0:
        messages.error(request, 'Product is out of stock.')
        return redirect('product_page:shop')

    # Check if the cart item already exists
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    # If item already exists in cart, check if adding one more exceeds stock
    if not item_created:
        if cart_item.quantity >= product.quantity:
            # Store error message in session
            request.session['product_error'] = {
                'product_id': product_id,
                'message': 'Maximum stock limit reached for this product.'
            }
            # Redirect to shop.html and display error message
            return redirect('product_page:shop-single', product_id=product.id)
        

        if cart_item.quantity >= product.max_qty_per_person:
            # Store error message in session
            request.session['product_error'] = {
                'product_id': product_id,
                'message': f'You can only add up to {product.max_qty_per_person} items of this product.'
            }
            # Redirect to shop-single.html and display error message
            return redirect('product_page:shop-single', product_id=product.id)

        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item.quantity = 1
        cart_item.save()

    messages.success(request, 'Product added to cart!')

    # Determine the referrer
    referrer = request.META.get('HTTP_REFERER', '')

    # Add messages based on referrer
    if 'shop-single' in referrer:
        
        
        return redirect('product_page:cart')

    # Redirect to shop.html and display success message
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
    return render(request,'user/checkout.html')
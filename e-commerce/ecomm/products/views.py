from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Brand, Size
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse


def shop(request):
    category_name = request.GET.get('category')
    brand_name = request.GET.get('brand')
    color = request.GET.get('color')
    size = request.GET.get('size')

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

    categories = Category.objects.all()
    brands = Brand.objects.filter(category__category_name=category_name) if category_name else Brand.objects.none()

    context = {
        'products': product_list,
        'categories': categories,
        'brands': brands,
        'selected_category': category_name,
        'selected_brand': brand_name,
        'selected_color': color,
        'selected_size': size,
    }
    return render(request, 'shop.html', context)

def shop_single(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    features_products = Product.objects.filter(trending=True)[:3]

    context = {
        'product': product,
        'featured_items': features_products
    }
    return render(request, 'shop-single.html', context)

def cart(request):
    return render(request, 'cart.html')


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
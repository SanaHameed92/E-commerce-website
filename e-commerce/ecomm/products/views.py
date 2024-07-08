from django.shortcuts import redirect, render,get_object_or_404
from . models import Product,Category
from django.core.paginator import Paginator

# Create your views here.
def shop(request):
    category_name = request.GET.get('category')
    product_list = Product.objects.all()
    if category_name:
        product_list = product_list.filter(category__category_name=category_name)

    product_paginator = Paginator(product_list,6)
    page_number = request.GET.get('page')
    product_list = product_paginator.get_page(page_number)
    categories = Category.objects.all() 
    context = {
        'products' : product_list,
        'categories' : categories,
        'selected_category': category_name
    }
    return render(request,'shop.html',context)


def shop_single(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    features_products = Product.objects.filter(trending=True)[:3]
    
    context = {
        'product': product,
        'featured_items' : features_products
    }
    return render(request, 'shop-single.html', context)

def cart(request):
    return render(request,'cart.html')





from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from .models import Product, Category
from categories.models import Category  # import from categories app
from .forms import ProductForm 

def home_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'products/home.html', {
        'products': products,
        'categories': categories,
    })

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    query = request.GET.get('q')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if category_id:
        products = products.filter(category_id=category_id)

    if query:
        products = products.filter(title__icontains=query)

    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    return render(request, 'products/list.html', {
        'products': products,
        'categories': categories,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/detail.html', {'product': product})


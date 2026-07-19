"""
FILE: views.py
PATH: shop/views.py
PURPOSE: Shop catalog views
DATA FLOW: Request -> Product Query -> Template
"""
from django.shortcuts import render, get_object_or_404
from .models import Product


def product_list(request):
    """Каталог товаров (Витрина)."""
    products = Product.objects.filter(is_available=True, stock__gt=0)
    context = {'products': products}
    return render(request, 'shop/product_list.html', context)


def product_detail(request, slug):
    """Детальная страница товара."""
    product = get_object_or_404(Product, slug=slug, is_available=True)
    context = {'product': product}
    return render(request, 'shop/product_detail.html', context)
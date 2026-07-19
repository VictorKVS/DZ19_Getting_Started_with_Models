"""
FILE: urls.py
PATH: shop/urls.py
PURPOSE: URL routes for shop catalog
"""
from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
]
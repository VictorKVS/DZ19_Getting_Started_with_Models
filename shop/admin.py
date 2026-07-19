"""
FILE: admin.py
PATH: shop/admin.py
PURPOSE: Admin interface for Product management
"""
from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'is_available', 'created_at')
    list_filter = ('is_available', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('price', 'stock', 'is_available')
    readonly_fields = ('created_at', 'updated_at')
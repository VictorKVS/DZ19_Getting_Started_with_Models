"""
FILE: models.py
PATH: shopping_cart/models.py
PURPOSE: Cart and CartItem models linked to real Products
DATA FLOW: User -> Cart -> CartItem -> Product
GUARANTEES: one Cart per user, atomic operations
"""
from django.db import models
from django.conf import settings


class Cart(models.Model):
    """Корзина пользователя."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart #{self.id} ({self.user.email})"
    
    def get_total(self):
        """Общая стоимость корзины."""
        return sum(item.get_subtotal() for item in self.items.all())
    
    def get_items_count(self):
        """Общее количество товаров."""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Товар в корзине (связан с реальным Product)."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(
        'shop.Product',
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    
    def get_subtotal(self):
        """Стоимость позиции."""
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity}"
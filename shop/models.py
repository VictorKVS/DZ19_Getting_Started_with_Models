"""
FILE: models.py
PATH: shop/models.py
PURPOSE: Product model for ORBITA PRIME catalog
DATA FLOW: Admin -> Product (DB) -> Shop Views -> Templates
GUARANTEES: price >= 0, stock >= 0, image optional
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    """Товар в каталоге ORBITA PRIME."""
    
    name = models.CharField(_('Название'), max_length=200)
    slug = models.SlugField(_('URL-идентификатор'), max_length=200, unique=True)
    description = models.TextField(_('Описание'), blank=True)
    price = models.DecimalField(
        _('Цена'),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    stock = models.PositiveIntegerField(
        _('Остаток на складе'),
        default=0,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(_('Изображение'), upload_to='products/', blank=True, null=True)
    is_available = models.BooleanField(_('Доступен для заказа'), default=True)
    created_at = models.DateTimeField(_('Создано'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Обновлено'), auto_now=True)
    
    class Meta:
        verbose_name = _('товар')
        verbose_name_plural = _('товары')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['-created_at']),
        ]
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('shop:product_detail', kwargs={'slug': self.slug})
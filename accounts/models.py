"""
FILE: models.py
PATH: accounts/models.py
PURPOSE: Custom user model with email as login + 152-FZ compliance
DATA FLOW: Forms -> Services -> CustomUser (DB) -> Views/Selectors
GUARANTEES: email unique, password hashed, is_active=False by default
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя для ORBITA PRIME."""
    
    # Аутентификационные поля
    email = models.EmailField(_('email адрес'), unique=True, max_length=255)
    
    # Персональные данные
    phone_number = models.CharField(_('номер телефона'), max_length=15, blank=True)
    address = models.TextField(_('адрес доставки'), max_length=500, blank=True)
    
    # Статусные поля
    is_active = models.BooleanField(_('активен'), default=False)  # False до подтверждения email
    is_staff = models.BooleanField(_('статус сотрудника'), default=False)
    date_joined = models.DateTimeField(_('дата регистрации'), auto_now_add=True)
    
    # 152-ФЗ: Согласие на обработку персональных данных
    pd_consent = models.BooleanField(_('согласие на обработку ПДн'), default=False)
    pd_consent_date = models.DateTimeField(_('дата согласия'), null=True, blank=True)
    pd_consent_ip = models.GenericIPAddressField(_('IP адрес при согласии'), null=True, blank=True)
    
    # Подключаем наш кастомный менеджер
    objects = CustomUserManager()
    
    # Указываем, что логинимся по email, а не по username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Email и пароль запрашиваются по умолчанию
    
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = _('пользователь')
        verbose_name_plural = _('пользователи')
        ordering = ['-date_joined']  # Новые пользователи отображаются первыми
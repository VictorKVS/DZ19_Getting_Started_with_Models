"""
FILE: managers.py
PATH: accounts/managers.py
PURPOSE: Custom user manager for creating users with email
DATA FLOW: create_user() -> normalize_email -> set_password -> save
GUARANTEES: password hashed, email normalized, superuser has is_staff=True
"""
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер, где email является уникальным идентификатором."""
    
    def create_user(self, email, password=None, **extra_fields):
        """Создание и сохранение обычного пользователя."""
        if not email:
            raise ValueError(_('Поле Email обязательно для заполнения'))
        
        # Приводим домен email к нижнему регистру (user@EXAMPLE.com -> user@example.com)
        email = self.normalize_email(email)
        
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # КРИТИЧНО: хеширует пароль, а не сохраняет как есть
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Создание и сохранение суперпользователя (администратора)."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)  # Суперпользователь активен сразу
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Суперпользователь должен иметь is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)
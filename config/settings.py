"""
FILE: settings.py
PATH: config/settings.py
PURPOSE: Central Django configuration for ORBITA PRIME
DATA FLOW: .env -> settings -> Django Core
GUARANTEES: AUTH_USER_MODEL before migrations, security headers enabled
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env (если он существует)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Безопасность: ключ берется из .env, иначе используется заглушка для разработки
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-dev-key-change-me-in-production')

# DEBUG и ALLOWED_HOSTS также можно управлять через .env
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Локальные приложения (accounts обязательно перед shopping_cart)
    'accounts',
    'shop',  
    'shopping_cart',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 8},
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ==============================================================================
# CRITICAL: Custom User Model (MUST be set BEFORE first migration!)
# ==============================================================================
AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'accounts:profile'
LOGOUT_REDIRECT_URL = 'accounts:login'

# ==============================================================================
# EMAIL SETTINGS (Умная маршрутизация: SMTP или Консоль)
# ==============================================================================
# Если в .env задан EMAIL_HOST, используем реальную отправку. Иначе — в консоль.
if os.getenv('EMAIL_HOST'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'noreply@orbitaprime.ru'
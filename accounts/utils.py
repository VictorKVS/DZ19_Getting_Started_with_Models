"""
FILE: urls.py
PATH: accounts/urls.py
PURPOSE: URL маршруты для приложения аутентификации
DATA FLOW: /accounts/* -> views
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Регистрация и активация (ЭТИХ СТРОК НЕ ХВАТАЛО)
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    # Вход и выход
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Личный кабинет
    path('profile/', views.profile, name='profile'),
]
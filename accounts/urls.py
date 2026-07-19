"""
FILE: urls.py
PATH: accounts/urls.py
PURPOSE: URL маршруты для приложения аутентификации
DATA FLOW: /accounts/* -> views
GUARANTEES: app_name для неймспейсинга, все маршруты auth
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Регистрация и активация
    path('register/', views.register, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    # Вход и выход
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Личный кабинет
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/delete/', views.delete_account, name='delete_account'),
    
    # Сброс пароля (встроенные Django views)
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt',
             success_url='/accounts/password_reset/done/'
         ), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url='/accounts/reset/done/'
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
    
    # Изменение пароля (для авторизованных)
    path('password_change/', 
         auth_views.PasswordChangeView.as_view(
             template_name='accounts/password_change.html',
             success_url='/accounts/password_change/done/'
         ), 
         name='password_change'),
    path('password_change/done/', 
         auth_views.PasswordChangeDoneView.as_view(
             template_name='accounts/password_change_done.html'
         ), 
         name='password_change_done'),
]
"""
FILE: views.py
PATH: accounts/views.py
PURPOSE: HTTP handlers for authentication flow
DATA FLOW: Request -> Form -> Model/Token -> Response
GUARANTEES: is_active check, secure token, audit logging, 152-FZ compliance
"""
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.utils import timezone

from .forms import CustomUserCreationForm, CustomAuthenticationForm, ProfileEditForm
from .models import CustomUser
from shopping_cart.utils import merge_session_cart

logger = logging.getLogger(__name__)


def get_client_ip(request):
    """Извлекает реальный IP-адрес клиента из заголовков запроса."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def register(request):
    """Обработка регистрации нового пользователя."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.pd_consent_ip = get_client_ip(request)
            user.pd_consent_date = timezone.now()
            user.save()
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            activation_link = request.build_absolute_uri(
                f'/accounts/activate/{uid}/{token}/'
            )
            
            send_mail(
                subject='Активация аккаунта ORBITA PRIME',
                message=f'Здравствуйте!\n\nПерейдите по ссылке для активации:\n{activation_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            
            logger.info(f"AUDIT | USER_REGISTERED | email={user.email} | ip={user.pd_consent_ip}")
            messages.success(request, 'Регистрация успешна! Проверьте консоль сервера для получения ссылки активации.')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'accounts/register.html', {'form': form})


def activate(request, uidb64, token):
    """Активация аккаунта по ссылке из email."""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=['is_active'])
        logger.info(f"AUDIT | USER_ACTIVATED | email={user.email}")
        messages.success(request, 'Аккаунт успешно активирован! Теперь вы можете войти.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Ссылка для активации недействительна или срок её действия истёк.')
        return redirect('accounts:register')


def user_login(request):
    """Вход в систему с проверкой статуса is_active и переносом корзины."""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            if not user.is_active:
                messages.error(request, 'Пожалуйста, подтвердите ваш email перед входом.')
                return redirect('accounts:login')
                
            login(request, user)
            logger.info(f"AUDIT | USER_LOGIN | email={user.email} | ip={get_client_ip(request)}")
            
            merge_session_cart(request, user)
            
            messages.success(request, f'Добро пожаловать на борт, {user.email}!')
            return redirect('accounts:profile')
    else:
        form = CustomAuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def profile(request):
    """Личный кабинет пользователя (Досье космонавта)."""
    # Получаем историю заказов (если модель Order существует)
    orders = []
    try:
        orders = request.user.orders.all()[:10]  # Последние 10 заказов
    except Exception:
        pass  # Если модели Order ещё нет, просто не показываем
    
    context = {
        'user': request.user,
        'orders': orders,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def edit_profile(request):
    """Редактирование профиля пользователя."""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            logger.info(f"AUDIT | PROFILE_UPDATED | email={request.user.email}")
            messages.success(request, 'Данные профиля успешно обновлены.')
            return redirect('accounts:profile')
    else:
        form = ProfileEditForm(instance=request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form': form})


@login_required
def delete_account(request):
    """Удаление аккаунта (право на забвение 152-ФЗ)."""
    if request.method == 'POST':
        user = request.user
        email = user.email
        user.delete()
        logger.info(f"AUDIT | ACCOUNT_DELETED | email={email} | ip={get_client_ip(request)}")
        messages.success(request, 'Ваш аккаунт и все персональные данные были удалены.')
        return redirect('home')
    
    return render(request, 'accounts/delete_account.html')


def user_logout(request):
    """Выход из системы."""
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('accounts:login')
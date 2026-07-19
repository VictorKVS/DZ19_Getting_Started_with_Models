"""
FILE: forms.py
PATH: accounts/forms.py
PURPOSE: Forms for user registration, authentication and profile editing
DATA FLOW: HTTP POST -> Form validation -> views
GUARANTEES: email uniqueness, pd_consent required, password validation
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации нового пользователя."""
    
    pd_consent = forms.BooleanField(
        required=True,
        label=_("Я даю согласие на обработку персональных данных в соответствии с 152-ФЗ"),
        error_messages={'required': _('Необходимо дать согласие на обработку персональных данных')}
    )
    
    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number', 'address', 'password1', 'password2', 'pd_consent')
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+79991234567'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Город, улица, дом'}),
        }

    def clean_email(self):
        """Проверка уникальности email."""
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(_('Этот email уже зарегистрирован в системе.'))
        return email


class CustomAuthenticationForm(AuthenticationForm):
    """Форма входа в систему (использует email вместо username)."""
    username = forms.EmailField(
        label=_('Email адрес'),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'autofocus': True, 'placeholder': 'email@example.com'})
    )
    password = forms.CharField(
        label=_('Пароль'),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'}),
    )


class ProfileEditForm(forms.ModelForm):
    """Форма редактирования профиля."""
    
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'address')
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+79991234567'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'phone_number': _('Канал связи (телефон)'),
            'address': _('База доставки (адрес)'),
        }
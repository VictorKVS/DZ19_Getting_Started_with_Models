from django.urls import path
from . import views

app_name = 'shopping_cart'

urlpatterns = [
    path('', views.view_cart, name='view'),
]

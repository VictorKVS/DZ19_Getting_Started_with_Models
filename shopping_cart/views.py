"""
FILE: views.py
PATH: shopping_cart/views.py
PURPOSE: Cart views (view, add, remove, clear)
DATA FLOW: Request -> Cart Service -> Template/Redirect
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Cart, CartItem
from shop.models import Product


@login_required
def view_cart(request):
    """Отображение корзины пользователя."""
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
        'total': cart.get_total(),
        'items_count': cart.get_items_count(),
    }
    return render(request, 'shopping_cart/cart.html', context)


@require_POST
def add_to_cart(request, product_id):
    """Добавление товара в корзину (работает и для анонимов через сессию)."""
    product = get_object_or_404(Product, id=product_id, is_available=True)
    
    if request.user.is_authenticated:
        # Авторизованный пользователь -> корзина в БД
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, product=product,
            defaults={'quantity': 1}
        )
        if not created:
            cart_item.quantity += 1
            cart_item.save(update_fields=['quantity'])
        messages.success(request, f'✅ "{product.name}" добавлен в корзину.')
    else:
        # Аноним -> корзина в сессии
        session_cart = request.session.get('cart', {})
        product_key = str(product.id)
        if product_key in session_cart:
            session_cart[product_key]['quantity'] += 1
        else:
            session_cart[product_key] = {
                'product_id': product.id,
                'product_name': product.name,
                'price': str(product.price),
                'quantity': 1,
            }
        request.session['cart'] = session_cart
        request.session.modified = True
        messages.success(request, f'✅ "{product.name}" добавлен в корзину.')
    
    return redirect(request.META.get('HTTP_REFERER', 'shop:product_list'))


@login_required
@require_POST
def remove_from_cart(request, item_id):
    """Удаление товара из корзины."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    product_name = cart_item.product.name
    cart_item.delete()
    messages.info(request, f'🗑️ "{product_name}" удалён из корзины.')
    return redirect('shopping_cart:view')


@login_required
@require_POST
def clear_cart(request):
    """Очистка всей корзины."""
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    messages.info(request, '🧹 Корзина очищена.')
    return redirect('shopping_cart:view')
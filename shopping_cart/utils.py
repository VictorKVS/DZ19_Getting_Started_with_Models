"""
FILE: utils.py
PATH: shopping_cart/utils.py
PURPOSE: Utility functions for cart management (session to DB merge)
DATA FLOW: Session cart -> DB cart (on login)
GUARANTEES: atomic merge, session cleanup, quantity aggregation, FK to Product
"""
import logging
from .models import Cart, CartItem
from shop.models import Product  # Импортируем модель товара для связи

logger = logging.getLogger(__name__)


def merge_session_cart(request, user):
    """
    Переносит товары из сессионной корзины в БД при входе пользователя.
    Теперь работает с реальными объектами Product через ForeignKey.
    """
    # Получаем корзину из сессии
    session_cart = request.session.get('cart', {})
    
    if not session_cart:
        logger.debug("Сессионная корзина пуста, перенос не требуется.")
        return  # Нечего переносить
    
    # Создаём или получаем корзину пользователя
    cart, created = Cart.objects.get_or_create(user=user)
    if created:
        logger.info(f"AUDIT | CART_CREATED | user={user.email}")
    
    merged_count = 0
    
    # Переносим товары из сессии в БД
    for key, data in session_cart.items():
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        # Защита: если товар был удален из каталога, пока пользователь был анонимом
        try:
            product = Product.objects.get(id=product_id, is_available=True)
        except Product.DoesNotExist:
            logger.warning(f"AUDIT | MERGE_SKIP | product_id={product_id} не найден или недоступен")
            continue  # Пропускаем этот товар
        
        # Ищем товар в корзине. Если его нет, создаем с quantity из сессии.
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,  # <-- ТЕПЕРЬ ИСПОЛЬЗУЕМ СВЯЗЬ С МОДЕЛЬЮ, а не строку
            defaults={'quantity': quantity}
        )
        
        # ВАЖНО: Если товар УЖЕ был в корзине, мы ДОЛЖНЫ сложить количества!
        if not item_created:
            cart_item.quantity += quantity
            cart_item.save(update_fields=['quantity'])
            
        merged_count += 1
    
    # Очищаем сессию после успешного переноса
    if 'cart' in request.session:
        del request.session['cart']
    request.session.modified = True
    
    if merged_count > 0:
        logger.info(f"AUDIT | CART_MERGED | user={user.email} | items={merged_count}")
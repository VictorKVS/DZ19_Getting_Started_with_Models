"""
FILE: test_utils.py
PATH: shopping_cart/tests/test_utils.py
PURPOSE: Integration tests for cart session merging
DATA FLOW: Test Request -> merge_session_cart -> DB Assertions
GUARANTEES: session cart is moved to DB, session is cleared, quantities aggregate

[Test Case setUp] --> (создание тестового пользователя)
[Test Case] --> (создание request.session['cart']) --> [merge_session_cart]
                                                  ↓
                                           [Cart / CartItem в БД]
                                                  ↓
[Test Case Assertions] <-- (проверка count, quantity, очистки сессии)

"""
from django.test import TestCase, RequestFactory
from accounts.models import CustomUser
from shopping_cart.models import Cart, CartItem
from shopping_cart.utils import merge_session_cart


class CartMergeUtilsTest(TestCase):
    """Тесты утилиты слияния корзины."""
    
    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом."""
        self.factory = RequestFactory()
        self.user = CustomUser.objects.create_user(
            email='cosmonaut@orbita.prime',
            password='SecurePass123!'
        )
        self.user.is_active = True
        self.user.save()
    
    def test_merge_session_cart_success(self):
        """T-CART-01: Успешный перенос товаров из сессии в БД."""
        # 1. Создаем запрос с сессионной корзиной
        request = self.factory.get('/cart/')
        request.session = self.client.session
        request.session['cart'] = {
            'Орбитальный полет (3 дня)': {'quantity': 1, 'price': 500000},
            'Невесомость (1 час)': {'quantity': 2, 'price': 50000},
        }
        request.session.save()
        
        # 2. Вызываем функцию слияния
        merge_session_cart(request, self.user)
        
        # 3. Проверяем, что корзина создана в БД
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 2)
        
        # 4. Проверяем корректность перенесенных данных
        item1 = cart.items.get(product_name='Орбитальный полет (3 дня)')
        self.assertEqual(item1.quantity, 1)
        self.assertEqual(item1.price, 500000)
        
        # 5. Проверяем, что сессия очищена
        self.assertNotIn('cart', request.session)
    
    def test_merge_empty_session_cart(self):
        """T-CART-02: Пустая сессия не вызывает ошибок и не создает корзину."""
        request = self.factory.get('/cart/')
        request.session = self.client.session
        # Сессия не содержит ключа 'cart'
        
        # Вызов не должен вызывать исключений
        merge_session_cart(request, self.user)
        
        # Корзина в БД не должна быть создана, так как переносить нечего
        self.assertFalse(Cart.objects.filter(user=self.user).exists())
        
    def test_merge_aggregates_quantities(self):
        """T-CART-03: Суммирование количества, если товар уже есть в БД."""
        # 1. Создаем корзину с одним товаром в БД
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product_name='Скафандр', quantity=1, price=100000)
        
        # 2. Добавляем тот же товар в сессию с количеством 2
        request = self.factory.get('/cart/')
        request.session = self.client.session
        request.session['cart'] = {
            'Скафандр': {'quantity': 2, 'price': 100000}
        }
        request.session.save()
        
        # 3. Вызываем слияние
        merge_session_cart(request, self.user)
        
        # 4. Проверяем, что количество суммировалось (1 + 2 = 3)
        cart.refresh_from_db()
        self.assertEqual(cart.items.count(), 1) # Все еще 1 уникальный товар
        item = cart.items.first()
        self.assertEqual(item.quantity, 3)
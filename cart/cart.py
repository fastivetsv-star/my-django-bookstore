from decimal import Decimal
from django.conf import settings
from products.models import Product

class Cart:
    def __init__(self, request):
        """Ініціалізуємо кошик з сесії клієнта."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Додаємо товар у кошик або оновлюємо його кількість."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        
        # Оновлюємо або додаємо кількість
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
            
        self.save()

    def save(self):
        """Повідомляємо Django, що сесія змінилася і її треба зберегти."""
        self.session.modified = True

    def remove(self, product):
        """Видаляємо товар з кошика."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """Повністю очищаємо кошик."""
        del self.session[settings.CART_SESSION_ID]
        self.save()
        
    def get_total_price(self):
        """Рахуємо загальну суму всіх товарів у кошику."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
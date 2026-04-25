import pytest
from .factories import OrderFactory
from products.tests.factories import ProductFactory
from orders.models import OrderItem

# Generated with AI, reviewed and modified
@pytest.mark.django_db
def test_order_str_method():
    """Перевіряємо, чи замовлення виводить правильний текст (напр: Замовлення #1)"""
    order = OrderFactory()
    assert str(order) == f"Замовлення #{order.id}"

# Generated with AI, reviewed and modified
@pytest.mark.django_db
def test_order_item_creation():
    """Перевіряємо, чи можемо ми додати товар у замовлення"""
    order = OrderFactory()
    product = ProductFactory(name="Мишка", price=50.00)
    
    # Створюємо OrderItem
    item = OrderItem.objects.create(
        order=order,
        product=product,
        price=product.price,
        quantity=2
    )
    
    assert item.order == order
    assert item.product.name == "Мишка"
    assert item.price == 50.00
    assert str(item) == f"Товар Мишка у замовленні #{order.id}"

# Generated with AI, reviewed and modified
@pytest.mark.django_db
def test_order_default_status():
    """Unit: Перевіряємо, чи нове замовлення завжди отримує статус 'pending'"""
    order = OrderFactory()
    assert order.status == "pending"

# Generated with AI, reviewed and modified
@pytest.mark.django_db
def test_order_default_email():
    """Unit: Перевіряємо, чи спрацьовує дефолтний email, якщо його не вказати"""
    from orders.models import Order
    order = Order.objects.create()
    assert order.email == "test@example.com"
    assert order.status == "pending"

# Generated with AI, reviewed and modified
@pytest.mark.django_db
@pytest.mark.parametrize("quantity", [1, 2, 10, 100])
def test_order_item_quantities(quantity):
    """Unit: Перевіряємо, чи OrderItem коректно зберігає будь-яку кількість"""
    order = OrderFactory()
    product = ProductFactory()
    item = OrderItem.objects.create(order=order, product=product, price=10.00, quantity=quantity)
    assert item.quantity == quantity
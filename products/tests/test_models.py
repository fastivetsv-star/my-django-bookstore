import pytest
from .factories import ProductFactory

@pytest.mark.django_db 
def test_product_creation():
    """Перевіряємо, чи фабрика коректно створює товар у базі даних"""
    product = ProductFactory()
    
    # Assert: Перевіряємо результати
    assert product.name == "Тестовий iPhone 15"
    assert product.price == 1000.00
    assert product.id is not None 

@pytest.mark.django_db
def test_product_str_method():
    """Перевіряємо, чи правильно товар відображається у вигляді рядка"""
    product = ProductFactory(name="Ноутбук Asus")
    assert str(product) == "Ноутбук Asus"

@pytest.mark.django_db
def test_category_str_method():
    """Перевіряємо відображення категорії"""
    from .factories import CategoryFactory
    category = CategoryFactory(name="Електроніка")
    assert str(category) == "Електроніка"
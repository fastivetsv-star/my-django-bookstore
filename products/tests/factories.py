import factory
from products.models import Product, Category # Обов'язково імпортуємо Category!

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "Тестова категорія"


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = "Тестовий iPhone 15"
    price = 1000.00
    
    category = factory.SubFactory(CategoryFactory)
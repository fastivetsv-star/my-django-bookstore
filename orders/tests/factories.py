import factory
from orders.models import Order

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    email = "test.client@example.com"
    status = "pending"
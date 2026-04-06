from django.db import models
from django.conf import settings
from products.models import Product 

class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Клієнт", null=True, blank=True)
    email = models.EmailField(verbose_name="Email для чека", default="test@example.com")
    status = models.CharField(max_length=20, default="pending", verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return f"Замовлення #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна під час покупки")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    def __str__(self):
        return f"Товар {self.product.name} у замовленні #{self.order.id}"
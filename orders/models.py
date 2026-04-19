from django.db import models
from django.conf import settings
from products.models import Product 
from django.utils.translation import gettext_lazy as _ # 👈 МАГІЧНИЙ ІМПОРТ

class Order(models.Model):
    # Загортаємо всі verbose_name у функцію _()
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=_("Клієнт"), null=True, blank=True)
    email = models.EmailField(verbose_name=_("Email для чека"), default="test@example.com")
    status = models.CharField(max_length=20, default="pending", verbose_name=_("Статус"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата створення"))

    class Meta:
        verbose_name = _("Замовлення")
        verbose_name_plural = _("Замовлення")

    def __str__(self):
        return f"Замовлення #{self.id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    
    # Тут теж загортаємо у _()
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Ціна під час покупки"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Кількість"))

    class Meta:
        verbose_name = _("Товар у замовленні")
        verbose_name_plural = _("Товари у замовленні")

    def __str__(self):
        return f"Товар {self.product.name} у замовленні #{self.order.id}"
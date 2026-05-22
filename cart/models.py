from django.db import models
from django.conf import settings
from products.models import Product
from django.utils.translation import gettext_lazy as _


class Cart(models.Model):
    # Корзина привязывается к пользователю (один к одному)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name=_("Клієнт"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Дата створення")
    )

    class Meta:
        verbose_name = _("Кошик")
        verbose_name_plural = _("Кошики")

    def __str__(self):
        return f"Кошик клієнта {self.user}"


class CartItem(models.Model):
    # Связь с корзиной и с товаром
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name=_("Товар")
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("Кількість"))

    class Meta:
        verbose_name = _("Товар у кошику")
        verbose_name_plural = _("Товари у кошику")

    def __str__(self):
        return f"{self.quantity} шт. {self.product.name} у кошику"

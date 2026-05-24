from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from products.models import Product
from .cart import Cart

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema


@require_POST
def cart_add(request, product_id):
    """
    Добавление товара в корзину через обычную форму на сайте.
    Работает на сессиях.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    cart.add(product=product)

    return redirect("product_list")


class CartViewSet(viewsets.ViewSet):
    """
    API-контроллер для работы с корзиной.
    Позволяет просматривать содержимое корзины через API.
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(responses=dict)
    def list(self, request):
        """
        Метод GET: Возвращает список товаров в корзине и общую сумму.
        """
        cart = Cart(request)

        cart_items = []

        # ИСПРАВЛЕНИЕ: Берем внутренний словарь cart.cart напрямую (как ты делал в заказах)
        # Если корзина пуста, берем пустой словарь {}
        cart_dict = cart.cart if hasattr(cart, "cart") else {}

        for item_id, item_data in cart_dict.items():
            # Создаем копию данных, чтобы случайно не изменить саму сессию
            item = item_data.copy()
            item["product_id"] = item_id

            # Достаем цену и количество
            price = item.get("price", 0)
            quantity = item.get("quantity", 1)

            # Превращаем цену в строку для правильного отображения в JSON
            item["price"] = str(price)

            # Считаем общую сумму для конкретного товара (цена * количество)
            if "total_price" not in item:
                item["total_price"] = str(float(price) * int(quantity))
            else:
                item["total_price"] = str(item["total_price"])

            # Очищаем от сложных объектов базы данных, если они есть
            if "product" in item:
                del item["product"]

            cart_items.append(item)

        # Безопасное получение финальной суммы всей корзины
        total_price = (
            str(cart.get_total_price()) if hasattr(cart, "get_total_price") else "0"
        )

        return Response({"cart_items": cart_items, "total_cart_price": total_price})

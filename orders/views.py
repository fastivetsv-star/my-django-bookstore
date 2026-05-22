import asyncio
import json
import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

# Импорты для REST API
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from .serializers import OrderSerializer

from .models import Order, OrderItem
from products.models import Product
from .services import create_payment_session
from cart.cart import Cart
from .tasks import send_order_email_task


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Order.objects.none()

        return (
            Order.objects.filter(customer=user)
            .prefetch_related("items")
            .order_by("-id")
        )

    def perform_create(self, serializer):
        with transaction.atomic():
            # Сохраняем заказ
            order = serializer.save(customer=self.request.user)
            # Отправляем письмо через Celery задачу
            send_order_email_task.delay(order.id)


def checkout_view(request):
    cart = Cart(request)

    if not cart.cart:
        return HttpResponse("Ваш кошик порожній! Додайте товари.")

    with transaction.atomic():
        order = Order.objects.create(
            customer=request.user if request.user.is_authenticated else None,
            email=(
                request.user.email
                if request.user.is_authenticated
                else "customer@example.com"
            ),
        )

        for item_id, item_data in cart.cart.items():
            product = Product.objects.get(id=item_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                price=item_data["price"],
                quantity=item_data["quantity"],
            )

        cart.clear()

    send_order_email_task.delay(order.id)

    payment_url = create_payment_session(order)
    return redirect(payment_url)


def success_view(request):
    return HttpResponse(
        "<h1>Ура! Оплата пройшла успішно! 🎉</h1><p>Ми вже пакуємо ваше замовлення.</p>"
    )


def cancel_view(request):
    return HttpResponse(
        "<h1>Оплата скасована 😢</h1><p>Нічого страшного, чекаємо вас знову!</p>"
    )


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        return HttpResponse(status=400)

    event_dict = json.loads(payload)

    if event_dict["type"] == "checkout.session.completed":
        session = event_dict["data"]["object"]
        order_id = session["metadata"]["order_id"]

        with transaction.atomic():
            order = Order.objects.get(id=order_id)

            total_order_price = sum(
                item.price * item.quantity for item in order.items.all()
            )
            expected_amount = int(total_order_price * 100)
            actual_amount = session.get("amount_total")

            if actual_amount != expected_amount:
                return HttpResponse(status=400)

            if session.get("payment_status") != "paid":
                return HttpResponse(status=400)

            order.status = "paid"
            order.save()
            print(f"🔒 ЗАХИЩЕНО І ОНОВЛЕНО: Замовлення #{order_id} успішно оплачено!")

    return HttpResponse(status=200)


def add_test_product(request):
    cart = Cart(request)
    product = Product.objects.first()
    if product:
        cart.add(product=product, quantity=1)
        return HttpResponse(
            f"Товар {product.name} додано в кошик! <a href='/checkout/'>Оформити замовлення</a>"
        )
    return HttpResponse("У базі немає товарів. Спочатку створи товар в адмінці!")

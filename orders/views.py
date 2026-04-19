from django.core.mail import send_mail
import json
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import redirect
from django.db import transaction
from .models import Order, OrderItem
from products.models import Product
from .services import create_payment_session
from cart.cart import Cart # Підключаємо твій новий кошик!
from .tasks import send_order_email_task

def checkout_view(request):
    cart = Cart(request)
    
    if not cart.cart:
        return HttpResponse("Ваш кошик порожній! Додайте товари.")

    with transaction.atomic():
        order = Order.objects.create(
            customer=request.user if request.user.is_authenticated else None,
            email="customer@example.com" 
        )
        
        for item_id, item_data in cart.cart.items():
            product = Product.objects.get(id=item_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                price=item_data['price'],
                quantity=item_data['quantity']
            )
        
        cart.clear()

    send_order_email_task.delay(order.id)

    payment_url = create_payment_session(order)
    return redirect(payment_url)

def success_view(request):
    return HttpResponse("<h1>Ура! Оплата пройшла успішно! 🎉</h1><p>Ми вже пакуємо ваше замовлення.</p>")

def cancel_view(request):
    return HttpResponse("<h1>Оплата скасована 😢</h1><p>Нічого страшного, чекаємо вас знову!</p>")

@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        return HttpResponse(status=400)

    event_dict = json.loads(payload)

    if event_dict['type'] == 'checkout.session.completed':
        session = event_dict['data']['object']
        order_id = session['metadata']['order_id']
        
        with transaction.atomic():
            order = Order.objects.get(id=order_id)
            
            total_order_price = sum(item.price * item.quantity for item in order.items.all())
            expected_amount = int(total_order_price * 100)
            actual_amount = session.get('amount_total')
            
            if actual_amount != expected_amount:
                return HttpResponse(status=400)
            
            if session.get('payment_status') != 'paid':
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
        return HttpResponse(f"Товар {product.name} додано в кошик! <a href='/checkout/'>Оформити замовлення</a>")
    return HttpResponse("У базі немає товарів. Спочатку створи товар в адмінці!")
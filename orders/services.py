import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_payment_session(order):
    # Збираємо всі товари з замовлення у список для Stripe
    line_items = []
    for item in order.items.all():
        line_items.append({
            "price_data": {
                "currency": "usd",
                "product_data": {
                    "name": item.product.name,
                },
                "unit_amount": int(item.price * 100), 
            },
            "quantity": item.quantity,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items, # Передаємо наш список товарів
        mode="payment",
        success_url="http://127.0.0.1:8000/success/", 
        cancel_url="http://127.0.0.1:8000/cancel/",
        metadata={"order_id": order.id}, 
    )
    return session.url
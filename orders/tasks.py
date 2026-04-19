from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from asgiref.sync import async_to_sync # Перехідник для WebSockets
from channels.layers import get_channel_layer # Інструмент для надсилання в канали

@shared_task
def send_order_email_task(order_id):
    order = Order.objects.get(id=order_id)
    

    subject = f'Замовлення №{order.id}'
    message = f'Дякуємо за замовлення #{order.id}! Ми вже почали його обробляти.'
    
    mail_sent = send_mail(
        subject,
        message,
        'admin@myshop.com',
        [order.email]
    )

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'notifications', 
        {
            'type': 'send_notification', 
            'message': f'Замовлення #{order.id} успішно оплачено! Лист відправлено клієнту.'
        }
    )

    return f"Лист для замовлення #{order.id} успішно відправлено!"
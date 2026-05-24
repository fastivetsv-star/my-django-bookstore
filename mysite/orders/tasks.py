from celery import shared_task
import time
from django.core.management import call_command


@shared_task
def send_order_email_task(order_id):
    """
    Асинхронна відправка email при створенні замовлення.
    Тепер вона не гальмуватиме відповідь сервера!
    """
    time.sleep(3)
    print(
        f"✅ УСПІХ: Лист для замовлення #{order_id} успішно відправлено клієнту у фоні!"
    )
    return f"Email sent for order {order_id}"


@shared_task
def generate_sales_report_task():
    """
    Періодичне завдання: генерація звітів.
    """
    time.sleep(5)
    print("📊 ЗВІТ: Щоденний звіт про продажі успішно згенеровано та збережено!")
    return "Report generated"


@shared_task
def clear_expired_sessions_task():
    """
    Періодичне завдання: очищення старих сесій користувачів з бази даних.
    Це вбудована команда Django, ми просто автоматизуємо її запуск.
    """
    call_command("clearsessions")
    print("🧹 ОЧИЩЕННЯ: Старі сесії успішно видалено з бази даних!")
    return "Sessions cleared"

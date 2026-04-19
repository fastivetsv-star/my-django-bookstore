import pytest
from unittest.mock import patch
from orders.tasks import send_order_email_task
from .factories import OrderFactory

@pytest.mark.django_db
@patch('orders.tasks.send_mail') 
def test_send_order_email_task(mock_send_mail):
    """Перевіряємо, чи Celery задача намагається відправити імейл"""
    
    order = OrderFactory()
    
    send_order_email_task(order.id)
    

    mock_send_mail.assert_called_once()
from django.test import TestCase
from unittest.mock import patch
from .services import process_payment_via_api

class PaymentServiceTest(TestCase):
    
    # Декоратор @patch перехоплює виклик requests.post всередині нашого services.py
    @patch('store.services.requests.post')
    def test_process_payment_success(self, mock_post):
        # 1. НАЛАШТУВАННЯ (Навчаємо наш фейковий запит, що він має відповісти)
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "id": 1,
            "order_id": 9999,
            "amount": "500.00",
            "status": "SUCCESS"
        }

        # 2. ДІЯ (Викликаємо нашу реальну функцію)
        result = process_payment_via_api(order_id=9999, amount="500.00")

        # 3. ПЕРЕВІРКА (Asserts)
        self.assertEqual(result['status'], "SUCCESS")
        self.assertEqual(result['order_id'], 9999)
        
        # Перевіряємо, чи функція взагалі намагалася зробити POST-запит
        mock_post.assert_called_once()
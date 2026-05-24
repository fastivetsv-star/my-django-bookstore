import requests
import logging

logger = logging.getLogger(__name__)

def process_payment_via_api(order_id, amount):
    url = "http://127.0.0.1:8000/api/payments/process/"
    
    payload = {
        "order_id": order_id,
        "amount": str(amount)
    }
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status() # Викине помилку, якщо статус не 2xx
        
        data = response.json()
        logger.info(f"Успішний платіж для замовлення {order_id}: {data}")
        return data
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Помилка API платежів для замовлення {order_id}: {e}")
        return {"status": "ERROR", "detail": "Платіжний сервіс тимчасово недоступний"}
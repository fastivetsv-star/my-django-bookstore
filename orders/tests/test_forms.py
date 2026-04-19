import pytest
from orders.forms import OrderCreateForm 

# ТЕСТ 1: Перевірка правильного імейла
def test_order_form_valid_data():
    form = OrderCreateForm(data={'email': 'good.client@example.com'})
    assert form.is_valid() is True

# ТЕСТ 2-6: П'ять тестів в одному за допомогою parametrize!
@pytest.mark.parametrize("bad_email", [
    "not-an-email",           # без @
    "user@.com",              # без домену
    "@example.com",           # без імені
    "user@example",           # без зони
    "",                       # порожній рядок
])
def test_order_form_invalid_emails(bad_email):
    """Цей тест автоматично запуститься 5 разів для кожного кривого імейла зі списку"""
    form = OrderCreateForm(data={'email': bad_email})
    assert form.is_valid() is False
    assert 'email' in form.errors
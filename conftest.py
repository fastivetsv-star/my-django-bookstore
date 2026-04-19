import pytest
from django.test import Client

@pytest.fixture
def client():
    """Створює віртуальний браузер (клієнт) для тестування views"""
    return Client()
import pytest
from django.urls import reverse
from .factories import ProductFactory

@pytest.mark.django_db
def test_product_list_view_status_code(client):
    """Перевіряємо, чи взагалі відкривається сторінка вітрини (статус 200)"""
    
    ProductFactory()
    

    url = reverse('product_list') 
    response = client.get(url)
    
    assert response.status_code == 200

@pytest.mark.django_db
def test_product_list_view_contains_product(client):
    """Перевіряємо, чи виводиться на сторінці назва нашого товару"""
    product = ProductFactory(name="Унікальний Супер Ноутбук")
    
    url = reverse('product_list')
    response = client.get(url)
    
    html_content = response.content.decode('utf-8')
    assert product.name in html_content
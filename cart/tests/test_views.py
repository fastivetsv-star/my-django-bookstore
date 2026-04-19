import pytest
from django.urls import reverse
from products.tests.factories import ProductFactory

@pytest.mark.django_db
def test_add_to_cart_flow(client):
    """Інтеграційний тест: Додавання товару в кошик"""
    
    product = ProductFactory(name="Тестові Навушники")
    
    url = reverse('cart_add', args=[product.id]) 
    
    response = client.post(url)
    
    assert response.status_code == 302 
    
    assert 'cart' in client.session


@pytest.mark.django_db
@pytest.mark.parametrize("url_name", [
    'product_list',  
 
])
def test_public_pages_render_correctly(client, url_name):
    """Інтеграційний: Перевірка, що головні сторінки не падають з помилкою 500"""
    url = reverse(url_name)
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
@pytest.mark.parametrize("invalid_id", [
    999,      
    99999,    
    0,        
])
def test_add_to_cart_not_found(client, invalid_id):
    """Інтеграційний: Що буде, якщо додати в кошик товар, якого не існує? (Має бути 404)"""
    
    url = reverse('cart_add', args=[invalid_id]) 
    
    response = client.post(url)
    assert response.status_code == 404

@pytest.mark.django_db
def test_add_to_cart_wrong_method(client):
    """Інтеграційний: Що буде, якщо звернутися до кошика через GET замість POST?"""
    product = ProductFactory()
    url = reverse('cart_add', args=[product.id])
    

    response = client.get(url)

    assert response.status_code != 200

@pytest.mark.django_db
def test_checkout_page_renders(client):
    """Інтеграційний: Перевіряємо, чи відкривається сторінка оформлення (checkout)"""
    url = reverse('checkout') 
    response = client.get(url)
    assert response.status_code == 200
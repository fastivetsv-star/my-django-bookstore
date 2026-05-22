from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class CartApiTests(TestCase):
    """
    Тесты для проверки API Корзины (Часть 2 из 3).
    """

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="buyer", email="buyer@test.com", password="testpassword"
        )

    def test_9_cart_access_denied_for_guests(self):
        """Тест 9: Анонимный пользователь получает ошибку 401 при попытке открыть корзину."""
        response = self.client.get("/api/cart/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_10_cart_access_allowed_for_users(self):
        """Тест 10: Авторизованный пользователь может открыть свою корзину."""
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/cart/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["total_cart_price"], "0")
        self.assertEqual(len(response.data["cart_items"]), 0)

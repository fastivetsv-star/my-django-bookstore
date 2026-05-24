from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch

from .models import Order
from products.models import Category, Product

User = get_user_model()


class OrdersAndAuthApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(
            username="buyer1", email="buyer1@test.com", password="strongpassword1"
        )

        self.user2 = User.objects.create_user(
            username="buyer2", email="buyer2@test.com", password="strongpassword2"
        )

        self.category = Category.objects.create(name="Тестовая Категория")
        self.product = Product.objects.create(
            category=self.category, name="Тестовый Товар", price="500.00"
        )

    def test_11_get_token_success(self):
        response = self.client.post(
            "/api/token/", {"username": "buyer1", "password": "strongpassword1"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_12_get_token_wrong_password(self):
        response = self.client.post(
            "/api/token/", {"username": "buyer1", "password": "wrong"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_13_get_token_no_data(self):
        response = self.client.post("/api/token/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_14_get_orders_guest(self):
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_15_create_order_guest(self):
        response = self.client.post("/api/orders/", {"email": "guest@test.com"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_16_delete_order_guest(self):
        order = Order.objects.create(customer=self.user1, email="buyer1@test.com")
        response = self.client.delete(f"/api/orders/{order.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_17_get_orders_auth_user(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/orders/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    @patch("orders.views.send_order_email_task.delay")
    def test_18_create_order_auth_user(self, mock_email_task):
        """Тест 18: Пользователь может успешно создать заказ (теперь с товаром!)."""
        self.client.force_authenticate(user=self.user1)

        # ДОБАВЛЕНО: Правильный формат данных с обязательным полем items
        payload = {
            "email": "buyer1@test.com",
            "items": [{"product": self.product.id, "quantity": 1, "price": "500.00"}],
        }

        response = self.client.post("/api/orders/", payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @patch("orders.views.send_order_email_task.delay")
    def test_19_order_auto_assign_customer(self, mock_email_task):
        self.client.force_authenticate(user=self.user1)

        payload = {
            "email": "buyer1@test.com",
            "items": [{"product": self.product.id, "quantity": 2, "price": "500.00"}],
        }

        response = self.client.post("/api/orders/", payload, format="json")
        order_id = response.data["id"]
        order = Order.objects.get(id=order_id)
        self.assertEqual(order.customer, self.user1)

    def test_20_get_specific_order_owner(self):
        order = Order.objects.create(customer=self.user1, email="buyer1@test.com")
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(f"/api/orders/{order.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_21_delete_own_order(self):
        order = Order.objects.create(customer=self.user1, email="buyer1@test.com")
        self.client.force_authenticate(user=self.user1)
        response = self.client.delete(f"/api/orders/{order.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_22_user_sees_only_own_orders(self):
        Order.objects.create(customer=self.user1, email="buyer1@test.com")
        self.client.force_authenticate(user=self.user2)
        response = self.client.get("/api/orders/")
        self.assertEqual(len(response.data["results"]), 0)

    def test_23_get_specific_order_not_owner(self):
        order = Order.objects.create(customer=self.user1, email="buyer1@test.com")
        self.client.force_authenticate(user=self.user2)
        response = self.client.get(f"/api/orders/{order.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_24_update_others_order(self):
        order = Order.objects.create(customer=self.user1, email="buyer1@test.com")
        self.client.force_authenticate(user=self.user2)
        response = self.client.patch(
            f"/api/orders/{order.id}/", {"email": "hacker@test.com"}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_25_delete_others_order(self):
        order = Order.objects.create(customer=self.user1, email="buyer1@test.com")
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f"/api/orders/{order.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

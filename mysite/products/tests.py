from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Product

User = get_user_model()


class ProductApiTests(TestCase):
    """
    Тесты для проверки API Товаров и Категорий (Часть 1 из 3).
    Здесь мы используем APIClient для имитации запросов.
    """

    def setUp(self):
        # Этот код выполняется перед КАЖДЫМ тестом
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            "admin", "admin@test.com", "adminpass"
        )

        # Создаем тестовую категорию
        self.category = Category.objects.create(name="Фантастика")

        # Создаем тестовые товары (УБРАЛИ поле description)
        self.product1 = Product.objects.create(
            category=self.category, name="Гарри Поттер", price="500.00"
        )
        self.product2 = Product.objects.create(
            category=self.category, name="Дюна", price="800.00"
        )

    # --- ТЕСТЫ ДЛЯ КАТЕГОРИЙ ---

    def test_1_get_categories_list_public(self):
        """Тест 1: Гость может получить список категорий."""
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["name"], "Фантастика")

    def test_2_create_category_forbidden_for_guest(self):
        """Тест 2: Гость НЕ может создать категорию."""
        data = {"name": "Новая"}
        response = self.client.post("/api/categories/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_3_create_category_by_admin(self):
        """Тест 3: Админ МОЖЕТ создать категорию."""
        self.client.force_authenticate(user=self.admin_user)
        data = {"name": "Романы"}
        response = self.client.post("/api/categories/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # --- ТЕСТЫ ДЛЯ ТОВАРОВ ---

    def test_4_get_products_list_public(self):
        """Тест 4: Гость может получить список товаров."""
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_5_create_product_forbidden_for_guest(self):
        """Тест 5: Гость НЕ может создать товар."""
        data = {"category": self.category.id, "name": "Новая книга", "price": "100.00"}
        response = self.client.post("/api/products/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_6_product_search_filter(self):
        """Тест 6: Проверка текстового поиска (search)."""
        response = self.client.get("/api/products/?search=Гарри")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Гарри Поттер")

    def test_7_product_ordering(self):
        """Тест 7: Проверка сортировки по цене (ordering)."""
        response = self.client.get("/api/products/?ordering=-price")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["name"], "Дюна")

    def test_8_product_category_filter(self):
        """Тест 8: Проверка фильтрации по ID категории."""
        response = self.client.get(f"/api/products/?category={self.category.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

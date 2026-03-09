from django.contrib import admin
from .models import Category, Book

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # Автоматическое заполнение поля slug на основе поля name

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'category')  # Отображение полей в списке книг
    list_filter = ('category', 'price')  # Фильтрация по категориям и цене
    search_fields = ('title', 'author')  # Поиск по названию и автору
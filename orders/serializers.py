from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Сериализатор для отдельных товаров в заказе.
    Документирует поля id, товар, цену и количество.
    """
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'price', 'quantity']
        read_only_fields = ['price'] 

class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для основного заказа.
    Включает в себя вложенный список товаров (items).
    """
    items = OrderItemSerializer(many=True) 

    class Meta:
        model = Order
        fields = ['id', 'customer', 'email', 'status', 'created_at', 'items']
        read_only_fields = ['customer', 'status', 'created_at']

    def create(self, validated_data):
        # 1. Извлекаем список товаров из данных
        items_data = validated_data.pop('items')
        
        # 2. ИСПРАВЛЕНИЕ: Безопасно удаляем customer из validated_data, если он там есть.
        # Это предотвращает ошибку "multiple values for keyword argument 'customer'".
        validated_data.pop('customer', None)
        
        # 3. Берем текущего пользователя из контекста запроса
        customer = self.context['request'].user
        
        # 4. Создаем основной заказ
        order = Order.objects.create(customer=customer, **validated_data)
        
        # 5. Создаем каждый товар, привязанный к этому заказу
        for item_data in items_data:
            product = item_data['product']
            OrderItem.objects.create(
                order=order, 
                product=product, 
                price=product.price, # Автоматически берем актуальную цену товара
                quantity=item_data['quantity']
            )
        return order
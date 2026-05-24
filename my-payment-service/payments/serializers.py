# payments/serializers.py
from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'order_id', 'amount', 'status', 'created_at']
        read_only_fields = ['status', 'created_at'] # Ці поля ми заповнюємо самі, а не клієнт
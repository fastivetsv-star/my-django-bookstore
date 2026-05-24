from django.shortcuts import render
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Transaction
from .serializers import TransactionSerializer

class ProcessPaymentView(APIView):
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        
        if serializer.is_valid():
            # Імітуємо відповідь від банку (наприклад, перевірка коштів на картці)
            payment_status = 'SUCCESS' if random.random() > 0.1 else 'FAILED'
            
            # Зберігаємо транзакцію в базу
            serializer.save(status=payment_status)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
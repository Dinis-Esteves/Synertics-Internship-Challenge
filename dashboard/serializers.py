# dashboard/serializers.py
from rest_framework import serializers
from .models import FuturesPrice

class FuturesPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuturesPrice
        fields = ['date', 'product_name', 'average_price']
        read_only_fields = fields  # Make all fields read-only for API
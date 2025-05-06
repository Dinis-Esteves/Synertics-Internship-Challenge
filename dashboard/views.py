from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime, timedelta
from .models import FuturesPrice
from .serializers import FuturesPriceSerializer

class FuturesDataAPIView(APIView):
    def get(self, request, format=None):
        # Calculate date range (last 7 days)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        # Get yearly baseload futures (GREBY*)
        queryset = FuturesPrice.objects.filter(
            product_name__startswith='GREBY',
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date')
        
        # Serialize the data
        serializer = FuturesPriceSerializer(queryset, many=True)
        
        # Calculate percentage changes
        data_with_changes = []
        previous_price = None
        
        for item in serializer.data:
            current_price = float(item['average_price'])
            
            # Calculate percentage change
            if previous_price is not None and previous_price != 0:
                percentage_change = ((current_price - previous_price) / previous_price) * 100
            else:
                percentage_change = 0
            
            # Add the calculated field
            enhanced_item = {
                **item,
                'percentage_change': round(percentage_change, 2),
                'date': item['date']  # Already formatted by the serializer
            }
            
            data_with_changes.append(enhanced_item)
            previous_price = current_price
        
        return Response({
            'status': 'success',
            'data': data_with_changes,
            'message': 'Futures data retrieved successfully'
        }, status=status.HTTP_200_OK)
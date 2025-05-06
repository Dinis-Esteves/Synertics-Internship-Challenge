from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import FuturesPrice
from .serializers import FuturesPriceSerializer

class FuturesDataAPIView(APIView):
    def get(self, request, format=None):
        # Date range: last 7 days
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)

        # Filter only GREBY26 product, last 7 days, sorted by date
        queryset = FuturesPrice.objects.filter(
            product_name='GREBY26',
            date__gte=start_date,
            date__lte=end_date
        ).order_by('date')

        # Serialize the data
        serializer = FuturesPriceSerializer(queryset, many=True)
        serialized_data = serializer.data

        # Calculate % change between first and last day (if enough data)
        if len(serialized_data) >= 2:
            first_price = float(serialized_data[0]['average_price'])
            last_price = float(serialized_data[-1]['average_price'])

            if first_price != 0:
                percentage_change = round(((last_price - first_price) / first_price) * 100, 2)
            else:
                percentage_change = None
        else:
            percentage_change = None

        return Response({
            'status': 'success',
            'data': serialized_data,
            'percentage_change': percentage_change,
            'message': 'Futures data for GREBY26 retrieved successfully'
        }, status=status.HTTP_200_OK)

def chart_view(request):
    return render(request, 'chart.html')

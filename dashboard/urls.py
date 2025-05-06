# dashboard/urls.py
from django.urls import path
from .views import FuturesDataAPIView, chart_view

urlpatterns = [
    path('api/futures-data/', FuturesDataAPIView.as_view(), name='futures-data'),
    path('chart/', chart_view, name='chart'),
]
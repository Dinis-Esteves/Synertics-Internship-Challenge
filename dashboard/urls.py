# dashboard/urls.py
from django.urls import path
from .views import FuturesDataAPIView

urlpatterns = [
    path('api/futures-data/', FuturesDataAPIView.as_view(), name='futures-data'),
]
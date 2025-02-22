# urls.py
from django.urls import path
from .views import PayoutsCreateView, PayoutsRetrieveUpdateDestroyView

urlpatterns = [
    path('payouts/', PayoutsCreateView.as_view(), name='payouts-create'),
    path('payouts/<str:artisan_unique_id>/', PayoutsRetrieveUpdateDestroyView.as_view(), name='payouts-retrieve-update-destroy'),
]
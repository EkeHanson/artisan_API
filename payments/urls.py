from django.urls import path
from .views import EscrowTransactionListCreateView

urlpatterns = [
    path('transactions/', EscrowTransactionListCreateView.as_view(), name='escrow-transactions'),
]

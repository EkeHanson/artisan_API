from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuotationViewSet

router = DefaultRouter()
router.register(r'quote_request', QuotationViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Ensure router URLs are included
]

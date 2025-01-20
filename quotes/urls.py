from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuotationViewSet

router = DefaultRouter()
router.register(r'quote_request', QuotationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

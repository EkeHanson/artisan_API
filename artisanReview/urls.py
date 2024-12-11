from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TradeReviewViewSet

router = DefaultRouter()
router.register(r'artisan-reviews', TradeReviewViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

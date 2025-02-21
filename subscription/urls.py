
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionPlanViewSet

# URLs
router = DefaultRouter()
router.register(r'subscriptions', SubscriptionPlanViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

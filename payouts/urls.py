
from .views import PayoutsViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'payouts', PayoutsViewSet, basename='payouts')

urlpatterns = [
    path('', include(router.urls)),
]

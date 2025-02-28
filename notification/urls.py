from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotoficationViewSet

router = DefaultRouter()
router.register(r'notification_request', NotoficationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

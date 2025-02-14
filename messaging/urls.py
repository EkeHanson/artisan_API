
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet

# Create a router instance
router = DefaultRouter()
router.register(r'messages', MessageViewSet, basename='message')

# Include the router's URLs
urlpatterns = [
    path('', include(router.urls)),
]

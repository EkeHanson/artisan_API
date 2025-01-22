
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MessageViewSet

router = DefaultRouter()
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]


#SEND MESSAGE ENDPOINT: /api/messages/send_message/
#REPLY MESSAGE ENDPOINT: /api/messages/{message_id}/reply/
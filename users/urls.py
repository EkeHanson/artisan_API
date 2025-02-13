from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, LoginView, ResetPasswordView, 
    ConfirmResetPasswordView, SendLoginTokenView, VerifyLoginTokenView, send_contact_email
)

router = DefaultRouter()
router.register(r'users', UserViewSet)  # Existing paginated user API

urlpatterns = [
    path('api/', include(router.urls)),  # Keeps paginated user list


    # Other existing endpoints
    path('api/user/<str:unique_id>/update/', UserViewSet.as_view({'patch': 'partial_update'}), name='user-update-by-id'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('send-contact-email/', send_contact_email, name='send_contact_email'),
    path('password-reset/', ResetPasswordView.as_view(), name='password-reset-request'),
    path('reset-password/<uidb64>/<token>/', ConfirmResetPasswordView.as_view(), name='reset-password'),
    path('api/send-login-token/', SendLoginTokenView.as_view(), name='send-login-token'),
    path('api/verify-login-token/', VerifyLoginTokenView.as_view(), name='verify-login-token'),
]

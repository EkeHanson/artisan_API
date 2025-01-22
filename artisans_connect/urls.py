from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView, TokenVerifyView
)


urlpatterns = [

    path('api/users/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),


    path('api/accounts/auth/', include('users.urls')), 
    path('api/jobs/auth/', include('jobs.urls')), 
    # path('api/tradeReviews/auth/', include('tradeReviews.urls')), 
    path('api/artisanReview/auth/', include('artisanReview.urls')), 
    path('api/profiles/auth/', include('profiles.urls')), 
    path('api/messaging/auth/', include('messaging.urls')), 
    path('api/payments/auth/', include('profiles.urls')), 
    path('api/quotes/', include('quotes.urls')),

    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

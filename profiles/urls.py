from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfileRequestViewSet, ArtisanByServiceDetailsView, ArtisanProfileByUniqueIdView


router = DefaultRouter()
router.register(r'artisan-profile', ProfileRequestViewSet)
# router.register(r'customerProfile', CustomerProfileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('artisans/by-service/<uuid:service_details_id>/', ArtisanByServiceDetailsView.as_view(), name='artisans-by-service'),
    path('artisan-profile/<uuid:unique_id>/', ArtisanProfileByUniqueIdView.as_view(), name='artisan-profile-by-unique-id'),
]

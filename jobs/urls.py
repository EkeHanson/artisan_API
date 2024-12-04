from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobRequestViewSet, ReviewViewSet, ServiceCategoryListCreateView, ServiceCategoryDetailView, BulkServiceCategoryCreateView


router = DefaultRouter()
router.register(r'jobs', JobRequestViewSet)
router.register(r'reviews', ReviewViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('service-categories/', ServiceCategoryListCreateView.as_view(), name='service-category-list'),
    
    path('service-categories/<int:pk>/', ServiceCategoryDetailView.as_view(), name='service-category-detail'),

    path('service-categories/bulk-create/', BulkServiceCategoryCreateView.as_view(), name='service-category-bulk-create'),
]

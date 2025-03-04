
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubscriptionPlanViewSet, UserSubscriptionViewSet, UserSubscriptionListView, UserSubscriptionDetailView

router = DefaultRouter()
router.register(r'subscriptions', SubscriptionPlanViewSet)
router.register(r'user-subscriptions', UserSubscriptionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),

    # path('payment-confirmation/', payment_confirmation, name='payment_confirmation'),

    path('api/user-subscription/<str:user_id>/', UserSubscriptionDetailView.as_view(), name='user_subscription_detail'),

    
    path('api/user-subscription/<str:user_id>/', UserSubscriptionDetailView.as_view(), name='user_subscription_detail'),
    
    path('api/user-subscriptions/<str:user_id>/', UserSubscriptionViewSet.as_view({'get': 'list'}), name='user_subscriptions_list'),

    path('api/user-multiple-subscriptions/<str:user_id>/', UserSubscriptionListView.as_view(), name='user_subscription_detail'),

]
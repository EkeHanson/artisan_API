# from rest_framework import viewsets
# from rest_framework.response import Response
# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework.exceptions import PermissionDenied
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from django.db.models import Q
# from uuid import UUID
# from .models import SubscriptionPlan
# from .serializers import SubscriptionPlanSerializer
# # from users.models import CustomUser

# # Create your views here.
# # Views
# class SubscriptionPlanViewSet(viewsets.ModelViewSet):
#     permission_classes = [AllowAny]
#     queryset = SubscriptionPlan.objects.all().order_by('id')  # Order by ID
#     serializer_class = SubscriptionPlanSerializer

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import SubscriptionPlan
from .serializers import SubscriptionPlanSerializer

class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = SubscriptionPlan.objects.all().order_by('id')  
    serializer_class = SubscriptionPlanSerializer

    def create(self, request, *args, **kwargs):
       # print("\n🔍 Incoming Request Data:", request.data)  # Debug: Print request payload
        
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("\n❌ Serializer Errors:", serializer.errors)  # Debug: Print validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

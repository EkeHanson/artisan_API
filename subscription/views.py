from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import SubscriptionPlan
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer, UserSubscriptionDetailSerializer
from dateutil.relativedelta import relativedelta
from .models import SubscriptionPlan, UserSubscription
from users.models import CustomUser
from rest_framework.decorators import action
from django.utils.timezone import now
from notification.models import  Notofication

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


class UserSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = UserSubscription.objects.all().order_by('id')
    serializer_class = UserSubscriptionSerializer
    permission_classes = [AllowAny]


    @action(detail=False, methods=['get'], url_path='active')
    def active_subscription(self, request):
        """
        GET /user-subscriptions/active/?user=<user_unique_id>
        Returns the only active subscription for the given user.
        """
        # Retrieve the user ID from the query parameters.
        user_id = request.query_params.get('user')
        if not user_id:
            return Response(
                {"detail": "User ID is required as a query parameter."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Strip any trailing slash or whitespace from the user_id
        user_id = user_id.rstrip('/').strip()

        # Attempt to fetch the user based on their unique_subscriber_id.
        try:
            user = CustomUser.objects.get(unique_subscriber_id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Filter for the user's active subscription:
        active_subscription = UserSubscription.objects.filter(
            user=user,
            is_active=True,
            end_date__gte=now().date()  # Ensure the subscription has not expired
        ).first()

        # If no active subscription is found, return an error response.
        if not active_subscription:
            return Response(
                {"detail": "No active subscription found for this user."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize and return the active subscription data.
        serializer = self.get_serializer(active_subscription)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Handle POST requests with detailed error logging."""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # Log and print the errors
            error_message = f"POST request errors: {serializer.errors}"
            print(error_message)  # Print to console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
                # Ensure subscribed_duration is provided
        subscribed_duration = request.data.get('subscribed_duration')
        if not subscribed_duration:
            return Response({'detail': 'Subscribed duration is required.'}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.data.get('user')
        subscription_plan_uuid = request.data.get('subscription_plan')

        if not user_id or not subscription_plan_uuid:
            error_message = "User ID and Subscription Plan UUID must be provided in the request."
            print(error_message)
            return Response({'detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(unique_id=user_id)
        except CustomUser.DoesNotExist:
            error_message = "The provided user does not exist or is not valid."
            print(error_message)
            return Response({'detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        # Check for any active or not yet expired subscriptions
        existing_subscriptions = UserSubscription.objects.filter(
            user=user,
            end_date__gte=now().date()  # Checks if there's any subscription that hasn't expired
        ).exists()

        # print(f"Found active subscriptions:")

        if existing_subscriptions:
            error_message = f"{user.first_name} {user.last_name} has an active  subscription and cannot subscribe again until the current subscription expires."
            print(error_message)
            return Response({'detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subscription_plan = SubscriptionPlan.objects.get(unique_id=subscription_plan_uuid)
        except SubscriptionPlan.DoesNotExist:
            error_message = "The selected subscription plan does not exist."
            return Response({'detail': error_message}, status=status.HTTP_400_BAD_REQUEST)

        subscription = serializer.save(user=user, subscription_plan=subscription_plan)

        # Ensure is_active is updated after saving
        subscription.is_active = True
        subscription.subscribing_user_name = f"{user.first_name}  {user.last_name}"
        subscription.save()
                    # ✅ Create a notification for the user
        Notofication.objects.create(
            customer=user,
            notification_message=f" {user.first_name} {user.last_name} has successfully subscribed to the {subscription_plan.name}.",
            notification_type="subscription_created"
        )

        # Update the organization's is_subscribed field to True
        user.is_subscribed = True
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserSubscriptionDetailView(generics.RetrieveAPIView):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionDetailSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return self.queryset.filter(user__unique_id=user_id)

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset)
        return obj

class UserSubscriptionListView(generics.ListAPIView):  # Change from RetrieveAPIView to ListAPIView
    permission_classes = [AllowAny]
    serializer_class = UserSubscriptionSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return UserSubscription.objects.filter(user__unique_id=user_id).order_by('-id')  # Return multiple records

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


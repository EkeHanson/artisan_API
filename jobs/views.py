from notification.models import  Notofication
# Create your views here.
from rest_framework.exceptions import NotFound
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework import viewsets
from .models import JobRequest, Review, ServiceCategory
from .serializers import JobRequestSerializer, ReviewSerializer, JobRequestCreateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from .models import ServiceCategory, JobRequest
from .serializers import ServiceCategorySerializer, ServiceCategoryBulkCreateSerializer, JobRequestSerializer
from rest_framework.views import APIView
from .serializers import ServiceCategoryBulkCreateSerializer, ServiceCategorySerializer


class BulkServiceCategoryCreateView(APIView):
    permission_classes = [AllowAny]
    """
    API endpoint to create multiple ServiceCategory records at once.
    """

    def post(self, request, *args, **kwargs):
        serializer = ServiceCategoryBulkCreateSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Service categories created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServiceCategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    """
    View to list all service categories and create a new one.
    """
    queryset = ServiceCategory.objects.all().order_by('id')
    serializer_class = ServiceCategorySerializer
    pagination_class = None  # Disable pagination for this view


class ServiceCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific service category.
    """
    queryset = ServiceCategory.objects.all().order_by('id')
    serializer_class = ServiceCategorySerializer


class JobRequestViewSet(viewsets.ModelViewSet):
    queryset = JobRequest.objects.all().order_by('-id')
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        unique_id = request.query_params.get('unique_id')
        if not unique_id:
            return Response({"error": "unique_id query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        job_profiles = JobRequest.objects.filter(unique_id=unique_id)

        if not job_profiles.exists():
            raise NotFound({"error": "ArtisanProfile with this unique_id does not exist."})

      
        serializer = JobRequestSerializer(job_profiles.first())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if self.action == 'create':
            return JobRequestCreateSerializer  # Use this for POST requests
        return JobRequestSerializer  # Use this for other CRUD operations
    

    @action(detail=False, methods=['get'], url_path='by-service')
    def get_jobs_by_service(self, request):
        service_id = request.query_params.get('service_details')

        if not service_id:
            return Response({"detail": "service_details parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        jobs = JobRequest.objects.filter(service_details__unique_id=service_id)

        if not jobs.exists():
            return Response({"detail": "No jobs found for this service."}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(jobs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def create(self, request, *args, **kwargs):
        """Handle POST requests with detailed error logging."""
        serializer = self.get_serializer(data=request.data)

        # print("request.data")
        # print(request.data)
        # print("request.data")

        if not serializer.is_valid():
            # Log and print the errors
            error_message = f"POST request errors: {serializer.errors}"
            print(error_message)  # Print to console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)

        # Create a notification for the job creation
        # print("request.data")
        # print(request.data)
        # print("request.data")
        # self.create_notification_for_job(request.data)
                # Save the job request
        job_request = serializer.save()

        # Create a notification for the job creation
        self.create_notification_for_job(job_request)
 
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create_notification_for_job(self, job_request):
        """
        Create a notification when a job is created.

        print
        """
        # print("job_request")
        # print(job_request)
        # print("job_request")
        try:
            # Fetch the customer and artisan (if applicable)
            customer = job_request.customer
            artisan = job_request.artisan  # Assuming artisan is linked to the job request

            # Create the notification message
            notification_message = f"A new job '{job_request.title}' has been created by {customer.first_name} {customer.last_name}."

            # Create the notification
            Notofication.objects.create(
                artisan=artisan,
                customer=customer,
                job_request=job_request,
                notification_message=notification_message,
            )
            print(f"Notification created for job: {job_request.unique_id}")
        except Exception as e:
            print(f"Error creating notification: {e}")

    def partial_update(self, request, *args, **kwargs):
        """Handle PATCH requests with detailed error logging."""
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            # Log and print the errors
            error_message = f"PATCH request errors: {serializer.errors}"
            print(error_message)  # Print to console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Custom action to filter jobs by user (using the user's unique_id)
    @action(detail=False, methods=['get'], url_path='user-jobs')
    def get_user_jobs(self, request):
        user_id = request.query_params.get('user_id')  # Expect user_id to be passed in query params
        
        if not user_id:
            return Response({"detail": "user_id parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter JobRequest objects by the customer (user)
        jobs = JobRequest.objects.filter(customer__unique_id=user_id)
        
        if not jobs:
            return Response({"detail": "No jobs found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize and return the filtered job requests
        serializer = self.get_serializer(jobs, many=True, context={'request': request})  # Pass request context to serializer
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

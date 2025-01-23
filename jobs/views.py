from django.shortcuts import render

# Create your views here.
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

# class JobRequestViewSet(viewsets.ModelViewSet):
#     queryset = JobRequest.objects.all().order_by('id')
#     serializer_class = JobRequestSerializer
#     permission_classes = [AllowAny]

#     def create(self, request, *args, **kwargs):
#         """Handle POST requests with detailed error logging."""
#         serializer = self.get_serializer(data=request.data)

#         print("request.data")
#         print(request.data)
#         print("request.data")
#         if not serializer.is_valid():
#             # Log and print the errors
#             error_message = f"POST request errors: {serializer.errors}"
#             print(error_message)  # Print to console
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         self.perform_create(serializer)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


#     def partial_update(self, request, *args, **kwargs):
#         """Handle PATCH requests with detailed error logging."""
#         partial = kwargs.pop('partial', True)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         if not serializer.is_valid():
#             # Log and print the errors
#             error_message = f"PATCH request errors: {serializer.errors}"
#             print(error_message)  # Print to console
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         self.perform_update(serializer)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     # Custom action to filter jobs by user (using the user's unique_id)
#     @action(detail=False, methods=['get'], url_path='user-jobs')
#     def get_user_jobs(self, request):
#         user_id = request.query_params.get('user_id')  # Expect user_id to be passed in query params
        
#         if not user_id:
#             return Response({"detail": "user_id parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
#         # Filter JobRequest objects by the customer (user)
#         jobs = JobRequest.objects.filter(customer__unique_id=user_id)
        
#         if not jobs:
#             return Response({"detail": "No jobs found for this user."}, status=status.HTTP_404_NOT_FOUND)
        
#         # Serialize and return the filtered job requests
#         serializer = JobRequestSerializer(jobs, many=True, context={'request': request})  # Pass request context to serializer
#         return Response(serializer.data, status=status.HTTP_200_OK)



class JobRequestViewSet(viewsets.ModelViewSet):
    queryset = JobRequest.objects.all().order_by('-id')
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'create':
            return JobRequestCreateSerializer  # Use this for POST requests
        return JobRequestSerializer  # Use this for other CRUD operations

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
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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

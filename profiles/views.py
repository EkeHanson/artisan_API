from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import ArtisanProfile
from .serializers import ArtisanProfileRequestSerializer
from django.db import IntegrityError
from rest_framework.views import APIView
from jobs.models import ServiceCategory
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination

class NoPagination(PageNumberPagination):
    page_size = None

class ArtisanProfilePagination(PageNumberPagination):
    page_size = 5  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow client to override, e.g., ?page_size=20
    max_page_size = 100  # Maximum allowed page size


class ArtisanProfileByUniqueIdView(APIView):
    permission_classes = [AllowAny]
    pagination_class = None  # Disable pagination for this view

    def get(self, request, *args, **kwargs):
        unique_id = request.query_params.get('unique_id')
        if not unique_id:
            return Response({"error": "unique_id query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        artisan_profiles = ArtisanProfile.objects.filter(user__unique_id=unique_id)

        if not artisan_profiles.exists():
            raise NotFound({"error": "ArtisanProfile with this unique_id does not exist."})

        if artisan_profiles.count() > 1:
            return Response({"error": "Multiple artisan profiles found for this unique_id. Data integrity issue."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ArtisanProfileRequestSerializer(artisan_profiles.first())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        unique_id = request.query_params.get('unique_id')
        if not unique_id:
            return Response({"error": "unique_id query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            artisan_profile = ArtisanProfile.objects.get(user__unique_id=unique_id)
        except ArtisanProfile.DoesNotExist:
            return Response({"error": "ArtisanProfile with this unique_id does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Convert request data to a mutable dictionary without using `.copy()`
        data = dict(request.data)  # Avoid `copy()` to prevent deep copying of file objects

        # Handle file uploads for qualifications
        qualifications_files = request.FILES.getlist('qualifications')
        if qualifications_files:
            if len(qualifications_files) > 5:
                return Response({"error": "You can only upload a maximum of 5 qualification files."}, status=status.HTTP_400_BAD_REQUEST)
            artisan_profile.qualifications.extend(qualifications_files)

        # Handle file uploads for previous jobs
        previous_jobs_files = request.FILES.getlist('previous_jobs')
        if previous_jobs_files:
            if len(previous_jobs_files) > 5:
                return Response({"error": "You can only upload a maximum of 5 previous job files."}, status=status.HTTP_400_BAD_REQUEST)
            artisan_profile.previous_jobs.extend(previous_jobs_files)

        # Remove file fields from data to prevent validation errors
        data.pop('qualifications', None)
        data.pop('previous_jobs', None)

        # Update the profile with the new data
        serializer = ArtisanProfileRequestSerializer(artisan_profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
        # print("serializer.errors")
        # print(serializer.errors)
        # print("serializer.errors")

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class NonPaginatedProfileRequestViewSet(viewsets.ModelViewSet):
#     """A ViewSet for listing Artisan Profiles without pagination."""
#     queryset = ArtisanProfile.objects.all().order_by('-id')
#     serializer_class = ArtisanProfileRequestSerializer
#     permission_classes = [AllowAny]
#     pagination_class = None  # ✅ Disable pagination for this viewset

#     def list(self, request, *args, **kwargs):
#         """Return all ArtisanProfiles without pagination."""
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)

class NonPaginatedProfileRequestViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing Artisan Profiles without pagination.
    """
    queryset = ArtisanProfile.objects.filter(user__is_approved=True).order_by('-id')
    serializer_class = ArtisanProfileRequestSerializer
    permission_classes = [AllowAny]
    pagination_class = None  # Disable pagination for this viewset

    def list(self, request, *args, **kwargs):
        """
        Return all approved ArtisanProfiles without pagination.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProfileRequestViewSet(viewsets.ModelViewSet):
    queryset = ArtisanProfile.objects.all().order_by('-id')
    serializer_class = ArtisanProfileRequestSerializer
    permission_classes = [AllowAny]
    pagination_class = ArtisanProfilePagination  # Use the custom pagination class

    def retrieve(self, request, *args, **kwargs):
        """Handle GET request for a single ArtisanProfile."""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        """Handle GET request for all ArtisanProfiles."""
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Handle POST requests with detailed error logging."""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            error_message = f"POST request errors: {serializer.errors}"
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.perform_create(serializer)
        except IntegrityError as e:
            error_message = "Foreign key constraint failed. Ensure the 'user' UUID exists and is an 'artisan'."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArtisanByServiceDetailsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, service_details_id, *args, **kwargs):
        try:
            # Retrieve the ServiceCategory using the provided ID
            service_details = ServiceCategory.objects.get(unique_id=service_details_id)

            # Filter ArtisanProfiles by the service_details
            artisans = ArtisanProfile.objects.filter(service_details=service_details)

            # Serialize the artisan profiles data
            serializer = ArtisanProfileRequestSerializer(artisans, many=True)

            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except ServiceCategory.DoesNotExist:
            return Response({"error": "ServiceCategory with this ID does not exist."}, status=status.HTTP_400_BAD_REQUEST)

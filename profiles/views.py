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

class ArtisanProfileByUniqueIdView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, unique_id, *args, **kwargs):
        try:
            # Retrieve ArtisanProfile using the provided unique_id
            artisan_profile = ArtisanProfile.objects.get(user__unique_id=unique_id)
            serializer = ArtisanProfileRequestSerializer(artisan_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ArtisanProfile.DoesNotExist:
            raise NotFound({"error": "ArtisanProfile with this unique_id does not exist."})


class ProfileRequestViewSet(viewsets.ModelViewSet):
    queryset = ArtisanProfile.objects.all().order_by('id')
    serializer_class = ArtisanProfileRequestSerializer
    permission_classes = [AllowAny]
    pagination_class = None  # Disable pagination for this view

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
            #print(error_message)  # Log the errors to the console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.perform_create(serializer)
        except IntegrityError as e:
            error_message = "Foreign key constraint failed. Ensure the 'user' UUID exists and is an 'artisan'."
            #print(f"Database Error: {e}")  # Log the error to the console
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

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
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import json

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
    

    # def patch(self, request, *args, **kwargs):
    #     print("request.data")
    #     print(request.data)
    #     print("request.data")
    #     unique_id = request.query_params.get("unique_id")
    #     if not unique_id:
    #         return Response({"error": "unique_id query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         artisan_profile = ArtisanProfile.objects.get(user__unique_id=unique_id)
    #     except ArtisanProfile.DoesNotExist:
    #         return Response({"error": "ArtisanProfile with this unique_id does not exist."}, status=status.HTTP_404_NOT_FOUND)

    #     # data = request.data.copy()
        

    #     # data = deepcopy(request.data)
    #     data = request.data.dict() if hasattr(request.data, "dict") else request.data
        
    #     file_fields = ['proof_of_address', 'international_passport', 'NIN_doc', 'other_doc', 'driver_licence']
    #     for field in file_fields:
    #         if field in request.FILES:
    #             setattr(artisan_profile, field, request.FILES[field])
        
    #     file_list_fields = {"qualifications": 5, "previous_jobs": 5}
    #     for field, max_files in file_list_fields.items():
    #         files = request.FILES.getlist(field)
    #         if files:
    #             if len(files) > max_files:
    #                 return Response({"error": f"You can only upload a maximum of {max_files} {field} files."}, status=status.HTTP_400_BAD_REQUEST)
    #             setattr(artisan_profile, field, files)
        
    #     for field in file_list_fields.keys():
    #         data.pop(field, None)
        
    #     serializer = ArtisanProfileRequestSerializer(artisan_profile, data=data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         print("serializer.data")
    #         print(serializer.data)
    #         print("serializer.data")
    #         return Response({"message": "Profile updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        
    #     print("serializer.errors")
    #     print(serializer.errors)
    #     print("serializer.errors")
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def patch(self, request, *args, **kwargs):
    #     print("request.data")
    #     print(request.data)
    #     print("request.data")

    #     unique_id = request.query_params.get("unique_id")
    #     if not unique_id:
    #         return Response({"error": "unique_id query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         artisan_profile = ArtisanProfile.objects.get(user__unique_id=unique_id)
    #     except ArtisanProfile.DoesNotExist:
    #         return Response({"error": "ArtisanProfile with this unique_id does not exist."}, status=status.HTTP_404_NOT_FOUND)

    #     data = request.data.dict() if hasattr(request.data, "dict") else request.data

    #     file_fields = ['proof_of_address', 'international_passport', 'NIN_doc', 'other_doc', 'driver_licence']
    #     for field in file_fields:
    #         if field in request.FILES:
    #             file_obj = request.FILES[field]
    #             file_path = default_storage.save(f"artisan_files/{file_obj.name}", ContentFile(file_obj.read()))
    #             setattr(artisan_profile, field, file_path)

    #     file_list_fields = {"qualifications": 5, "previous_jobs": 5}

    #     for field, max_files in file_list_fields.items():
    #         files = request.FILES.getlist(field)

    #         # Retrieve existing files safely
    #         existing_files = getattr(artisan_profile, field, "[]")
    #         if isinstance(existing_files, str):  # Convert JSON string to list if necessary
    #             existing_files = json.loads(existing_files)
    #         elif not isinstance(existing_files, list):  # Ensure it's always a list
    #             existing_files = []

    #         print(f"Existing {field}: {len(existing_files)}")
    #         print(f"Newly uploaded {field}: {len(files)}")

    #         if files:
    #             total_files = len(existing_files) + len(files)

    #             if total_files > max_files:
    #                 return Response(
    #                     {
    #                         "error": f"You can only upload {max_files} {field} files in total. "
    #                                 f"You currently have {len(existing_files)} files."
    #                     },
    #                     status=status.HTTP_400_BAD_REQUEST
    #                 )

    #             # Save new files
    #             saved_file_paths = existing_files[:]  # Keep a copy of existing files
    #             for file_obj in files:
    #                 file_path = default_storage.save(f"artisan_files/{file_obj.name}", ContentFile(file_obj.read()))
    #                 saved_file_paths.append(file_path)

    #             setattr(artisan_profile, field, json.dumps(saved_file_paths))  # Save as JSON string






    #     for field in file_list_fields.keys():
    #         data.pop(field, None)

    #     serializer = ArtisanProfileRequestSerializer(artisan_profile, data=data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         print("serializer.data")
    #         print(serializer.data)
    #         print("serializer.data")
    #         return Response({"message": "Profile updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    #     print("serializer.errors")
    #     print(serializer.errors)
    #     print("serializer.errors")
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




    # def patch(self, request, *args, **kwargs):
    #     print("request.data")
    #     print(request.data)
    #     print("request.data")

    #     unique_id = request.query_params.get("unique_id")
    #     if not unique_id:
    #         return Response({"error": "unique_id query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

    #     try:
    #         artisan_profile = ArtisanProfile.objects.get(user__unique_id=unique_id)
    #     except ArtisanProfile.DoesNotExist:
    #         return Response({"error": "ArtisanProfile with this unique_id does not exist."}, status=status.HTTP_404_NOT_FOUND)

    #     data = request.data.dict() if hasattr(request.data, "dict") else request.data

    #     # Handle Single File Fields (Proof of Address, Passport, etc.)
    #     file_fields = ['proof_of_address', 'international_passport', 'NIN_doc', 'other_doc', 'driver_licence']
    #     for field in file_fields:
    #         if field in request.FILES:
    #             file_obj = request.FILES[field]
    #             file_path = default_storage.save(f"artisan_files/{file_obj.name}", ContentFile(file_obj.read()))
    #             setattr(artisan_profile, field, file_path)

    #     # Handle Multiple File Fields (Qualifications & Previous Jobs)
    #     file_list_fields = {"qualifications": 5, "previous_jobs": 5}

    #     for field, max_files in file_list_fields.items():
    #         files = request.FILES.getlist(field)

    #         if files:
    #             if len(files) > max_files:
    #                 return Response(
    #                     {"error": f"You can only upload up to {max_files} {field} files at once."},
    #                     status=status.HTTP_400_BAD_REQUEST,
    #                 )

    #             # **Ensure New Uploads Replace Old Files**
    #             saved_file_paths = []
    #             for file_obj in files:
    #                 file_path = default_storage.save(f"artisan_files/{file_obj.name}", ContentFile(file_obj.read()))
    #                 saved_file_paths.append(file_path)

    #             setattr(artisan_profile, field, json.dumps(saved_file_paths))  # Save as JSON string

    #     # Remove file fields from data before serialization
    #     for field in file_list_fields.keys():
    #         data.pop(field, None)

    #     serializer = ArtisanProfileRequestSerializer(artisan_profile, data=data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         print("serializer.data")
    #         print(serializer.data)
    #         print("serializer.data")
    #         return Response({"message": "Profile updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    #     print("serializer.errors")
    #     print(serializer.errors)
    #     print("serializer.errors")
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, *args, **kwargs):
        # print("request.data")
        # print(request.data)
        # print("request.data")

        unique_id = request.query_params.get("unique_id")
        if not unique_id:
            return Response({"error": "unique_id query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            artisan_profile = ArtisanProfile.objects.get(user__unique_id=unique_id)
        except ArtisanProfile.DoesNotExist:
            return Response({"error": "ArtisanProfile with this unique_id does not exist."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.dict() if hasattr(request.data, "dict") else request.data

        # Handle Single File Fields (Proof of Address, Passport, etc.)
        file_fields = ['proof_of_address', 'international_passport', 'NIN_doc', 'other_doc', 'driver_licence']
        for field in file_fields:
            if field in request.FILES:
                file_obj = request.FILES[field]
                file_path = default_storage.save(f"artisan_files/{file_obj.name}", ContentFile(file_obj.read()))
                setattr(artisan_profile, field, file_path)

        # Handle Multiple File Fields (Qualifications & Previous Jobs)
        file_list_fields = {"qualifications": 5, "previous_jobs": 5}

        for field, max_files in file_list_fields.items():
            files = request.FILES.getlist(field)

            if files:
                # Get the current files for the field
                current_files = getattr(artisan_profile, field, []) or []

                # Add new files to the list
                for file_obj in files:
                    file_path = default_storage.save(f"artisan_files/{file_obj.name}", ContentFile(file_obj.read()))
                    current_files.append(file_path)

                # If the total number of files exceeds the limit, remove the oldest files
                if len(current_files) > max_files:
                    # Remove the oldest files (first in the list)
                    num_files_to_remove = len(current_files) - max_files
                    for _ in range(num_files_to_remove):
                        file_to_remove = current_files.pop(0)
                        # Delete the file from storage
                        default_storage.delete(file_to_remove)

                # Update the field with the new list of files
                setattr(artisan_profile, field, current_files)

        # Remove file fields from data before serialization
        for field in file_list_fields.keys():
            data.pop(field, None)

        serializer = ArtisanProfileRequestSerializer(artisan_profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # print("serializer.data")
            # print(serializer.data)
            # print("serializer.data")
            return Response({"message": "Profile updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

        # print("serializer.errors")
        # print(serializer.errors)
        # print("serializer.errors")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

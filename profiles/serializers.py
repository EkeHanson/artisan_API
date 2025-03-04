from rest_framework import serializers
from django.core.validators import FileExtensionValidator
from .models import ArtisanProfile
from users.models import CustomUser
from jobs.models import ServiceCategory
from rest_framework.response import Response
from rest_framework import status, serializers
from django.core.validators import FileExtensionValidator
import os
import json

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'unique_id',
            'email',
            'phone',
            'first_name',
            'last_name',
            'user_type',
            'date_joined',
            'is_approved',
            'identification_code',
        ]

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = [
            'unique_id',
            'name',
            'postName',
            'simpleDescription',
            'complexDescription',
            'services',
        ]

# class ArtisanProfileRequestSerializer(serializers.ModelSerializer):
#     service_details = ServiceCategorySerializer(read_only=True)  # Read-only for GET requests
#     service_details_id = serializers.UUIDField(write_only=True)  # Write-only for POST requests
#     user = CustomUserSerializer(read_only=True)  # Read-only for GET requests
#     user_id = serializers.UUIDField(write_only=True)  # Write-only for POST requests

#     # qualifications = serializers.ListField(
#     #     child=serializers.FileField(), required=False
#     # )
#     # previous_jobs = serializers.ListField(
#     #     child=serializers.FileField(), required=False
#     # )
#     def validate_proof_of_address(self, value):
#         self.validate_file_type(value)
#         return value

#     def validate_NIN_doc(self, value):
#         self.validate_file_type(value)
#         return value

#     def validate_other_doc(self, value):
#         self.validate_file_type(value)
#         return value
#     def validate_driver_licence(self, value):
#         self.validate_file_type(value)
#         return value
    
#     def validate_international_passport(self, value):
#         self.validate_file_type(value)
#         return value

#     def validate_file_type(self, value):
#         import os
#         valid_extensions = ['.png', '.jpg', '.jpeg', '.pdf']
#         ext = os.path.splitext(value.name)[1]  # Extract file extension
#         if ext.lower() not in valid_extensions:
#             raise serializers.ValidationError(f'Unsupported file format. Allowed formats: PNG, JPG, JPEG, PDF')
        
#     qualifications = serializers.ListField(
#         child=serializers.FileField(
#             allow_empty_file=False,
#             validators=[FileExtensionValidator(allowed_extensions=['png', 'pdf', 'jpg', 'jpeg'])]
#         ),
#         required=False
#     )

#     previous_jobs = serializers.ListField(
#         child=serializers.FileField(
#             allow_empty_file=False,
#             validators=[FileExtensionValidator(allowed_extensions=['png', 'pdf', 'jpg', 'jpeg'])]
#         ),
#         required=False
#     )


#     class Meta:
#         model = ArtisanProfile
#         fields = '__all__'

#     def validate_user_id(self, value):
#         """Validate that the provided user ID corresponds to a valid 'artisan'."""
#         try:
#             user = CustomUser.objects.get(unique_id=value)
#             if user.user_type != 'artisan':
#                 raise serializers.ValidationError("The user must be of type 'artisan'.")
#         except CustomUser.DoesNotExist:
#             raise serializers.ValidationError("User with this ID does not exist.")
#         return value

#     def validate_service_details_id(self, value):
#         """Validate that the provided service_details ID corresponds to a valid 'ServiceCategory'."""
#         try:
#             service_details = ServiceCategory.objects.get(unique_id=value)
#         except ServiceCategory.DoesNotExist:
#             raise serializers.ValidationError("ServiceCategory with this ID does not exist.")
#         return value

#     def create(self, validated_data):
#         # Retrieve user and service_details based on provided IDs
#         user_id = validated_data.pop('user_id')
#         service_details_id = validated_data.pop('service_details_id')

#         user = CustomUser.objects.get(unique_id=user_id)  # Retrieve the user based on the ID
#         service_details = ServiceCategory.objects.get(unique_id=service_details_id)  # Retrieve the ServiceCategory

#         # Create ArtisanProfile
#         artisan_profile = ArtisanProfile.objects.create(user=user, service_details=service_details, **validated_data)
#         return artisan_profile


class ArtisanProfileRequestSerializer(serializers.ModelSerializer):
    service_details = ServiceCategorySerializer(read_only=True)
    service_details_id = serializers.UUIDField(write_only=True)
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.UUIDField(write_only=True)
    
    qualifications = serializers.SerializerMethodField()
    previous_jobs = serializers.SerializerMethodField()

    file_fields = ['proof_of_address', 'international_passport', 'NIN_doc', 'other_doc', 'driver_licence']

    def validate_file_type(self, value):
        valid_extensions = ['.png', '.jpg', '.jpeg', '.pdf']
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError(f'Unsupported file format. Allowed formats: PNG, JPG, JPEG, PDF')
        return value

    for field in file_fields:
        locals()[f'validate_{field}'] = validate_file_type



    def get_qualifications(self, obj):
        return obj.qualifications if obj.qualifications else []

    def get_previous_jobs(self, obj):
        return obj.previous_jobs if obj.previous_jobs else []


    class Meta:
        model = ArtisanProfile
        fields = '__all__'

    def validate_user_id(self, value):
        try:
            user = CustomUser.objects.get(unique_id=value)
            if user.user_type != 'artisan':
                raise serializers.ValidationError("The user must be of type 'artisan'.")
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist.")
        return value

    def validate_service_details_id(self, value):
        try:
            ServiceCategory.objects.get(unique_id=value)
        except ServiceCategory.DoesNotExist:
            raise serializers.ValidationError("ServiceCategory with this ID does not exist.")
        return value


from rest_framework import serializers
from users.models import CustomUser
from jobs.models import JobRequest
from .models import Notofication

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "unique_id",
            "email",
            "phone",
            "first_name",
            "last_name",
            "user_type",
            "date_joined",
        ]

class JobRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRequest
        fields = [
            "unique_id",
            "customer",
            "title",
            "description",
            "num_appllications",
            "location",
            "service_description",
            "created_at",
            "artisan_done",
            "customer_done",
            "admin_done",
  
        ]

class NotoficationRequestSerializer(serializers.ModelSerializer):
    job_request = JobRequestSerializer(read_only=True)  # Read-only for GET requests
    job_request_id = serializers.UUIDField(write_only=True)  # Write-only for POST requests
    artisan = CustomUserSerializer(read_only=True)  # Read-only for GET requests
    customer = CustomUserSerializer(read_only=True)  # Read-only for GET requests
    artisan_id = serializers.UUIDField(write_only=True)  # Write-only for POST requests
    customer_id = serializers.UUIDField(write_only=True)  # Write-only for POST requests

    class Meta:
        model = Notofication
        fields = [
            "unique_id",
            "artisan",
            "customer",

            "artisan_id",
            "customer_id",

            "job_request",
            "job_request_id",
            
            "notification_message",

            "created_at",
        ]

  

    def create(self, validated_data):
        """Create a Notification with validated artisan, customer, and job request."""
        artisan_id = validated_data.pop("artisan_id")
        customer_id = validated_data.pop("customer_id")
        job_request_id = validated_data.pop("job_request_id")

        artisan = CustomUser.objects.get(unique_id=artisan_id)
        customer = CustomUser.objects.get(unique_id=customer_id)
        job_request = JobRequest.objects.get(unique_id=job_request_id)

        validated_data["artisan"] = artisan
        validated_data["customer"] = customer
        validated_data["job_request"] = job_request

        return super().create(validated_data)




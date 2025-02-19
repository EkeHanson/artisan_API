from rest_framework import serializers
from .models import QuoteRequest
from users.models import CustomUser
from jobs.models import JobRequest

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
            "about_artisan",
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
        ]

class QuoteRequestSerializer(serializers.ModelSerializer):
    job_request = JobRequestSerializer(read_only=True)  # Read-only for GET requests
    job_request_id = serializers.UUIDField(write_only=True)  # Write-only for POST requests
    artisan = CustomUserSerializer(read_only=True)  # Read-only for GET requests
    artisan_id = serializers.UUIDField(write_only=True)  # Write-only for POST requests

    class Meta:
        model = QuoteRequest
        fields = [
            "unique_id",
            "artisan",
            "artisan_id",
            "job_request",
            "job_request_id",
            "bid_amount",
            "freelancer_service_fee",
            "job_duration",
            "created_at",
        ]

    def validate(self, data):
        """Ensure an artisan can only submit one quote per job."""
        artisan_id = data.get("artisan_id")
        job_request_id = data.get("job_request_id")

        if QuoteRequest.objects.filter(artisan__unique_id=artisan_id, job_request__unique_id=job_request_id).exists():
            raise serializers.ValidationError("You have already submitted a quote for this job.")

        return data

    def create(self, validated_data):
        """Create a QuoteRequest with validated artisan and job request."""
        artisan_id = validated_data.pop("artisan_id")
        job_request_id = validated_data.pop("job_request_id")

        artisan = CustomUser.objects.get(unique_id=artisan_id)
        job_request = JobRequest.objects.get(unique_id=job_request_id)

        validated_data["artisan"] = artisan
        validated_data["job_request"] = job_request

        return super().create(validated_data)

from .models import JobRequest, Review, ServiceCategory
from rest_framework import serializers


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = "__all__"

class BulkServiceCategorySerializer(serializers.ListSerializer):
    """
    Serializer to handle bulk creation of ServiceCategory records.
    """

    def create(self, validated_data):
        return ServiceCategory.objects.bulk_create([ServiceCategory(**item) for item in validated_data])


class ServiceCategoryBulkCreateSerializer(serializers.ModelSerializer):
    """
    Use this serializer for bulk creation.
    """

    class Meta:
        model = ServiceCategory
        list_serializer_class = BulkServiceCategorySerializer
        fields = "__all__"



class JobRequestSerializer(serializers.ModelSerializer):
    status = serializers.CharField(default='open')
    class Meta:
        model = JobRequest
        fields ="__all__"
        # fields = ['id', 'title', 'description', 'location', 'budget', 'created_at', 'status', 'artisan']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        # fields = ['job', 'customer', 'artisan', 'rating', 'comment', 'created_at']



# from .models import JobRequest, Review, ServiceCategory
# from rest_framework import serializers


# class ServiceCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ServiceCategory
#         fields = "__all__"

# class BulkServiceCategorySerializer(serializers.ListSerializer):
#     """
#     Serializer to handle bulk creation of ServiceCategory records.
#     """

#     def create(self, validated_data):
#         return ServiceCategory.objects.bulk_create([ServiceCategory(**item) for item in validated_data])


# class ServiceCategoryBulkCreateSerializer(serializers.ModelSerializer):
#     """
#     Use this serializer for bulk creation.
#     """

#     class Meta:
#         model = ServiceCategory
#         list_serializer_class = BulkServiceCategorySerializer
#         fields = "__all__"


# class JobRequestSerializer(serializers.ModelSerializer):
#     status = serializers.CharField(default='open')
#     class Meta:
#         model = JobRequest
#         fields ="__all__"
#         # fields = ['id', 'title', 'description', 'location', 'budget', 'created_at', 'status', 'artisan']

# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = "__all__"
#         # fields = ['job', 'customer', 'artisan', 'rating', 'comment', 'created_at']




from .models import JobRequest, Review, ServiceCategory
from rest_framework import serializers
from rest_framework import serializers
from .models import JobRequest, ServiceCategory


class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = "__all__"  # Return all fields for ServiceCategory

# class JobRequestCreateSerializer(serializers.ModelSerializer):
#     status = serializers.CharField(default='open')
#     service_details = serializers.PrimaryKeyRelatedField(queryset=ServiceCategory.objects.all())  # Accept UUIDs

#     class Meta:
#         model = JobRequest
#         fields = "__all__"  # Include all fields from JobRequest

class JobRequestCreateSerializer(serializers.ModelSerializer):
    status = serializers.CharField(default='open')
    class Meta:
        model = JobRequest
        fields ="__all__"
        # fields = ['id', 'title', 'description', 'location', 'budget', 'created_at', 'status', 'artisan']


class JobRequestSerializer(serializers.ModelSerializer):
    status = serializers.CharField(default='open')
    # service_details = serializers.PrimaryKeyRelatedField(queryset=ServiceCategory.objects.all())

    service_details = ServiceCategorySerializer()  # Use ServiceCategorySerializer for nested serialization

    class Meta:
        model = JobRequest
        fields = "__all__"  # Include all fields from JobRequest

    def to_representation(self, instance):
        """
        Customize the representation of JobRequest to only return 'name' and 'postName' for the service_details field
        during GET requests for JobRequest, without affecting the POST request format.
        """
        representation = super().to_representation(instance)
        
        # Check if it's a GET request for JobRequest (not for ServiceCategory)
        if self.context.get('request') and self.context['request'].method == 'GET':
            # Modify the service_details field to include only name and postName
            service_details_data = representation.get('service_details', {})
            if service_details_data:
                representation['service_details'] = {
                    'name': service_details_data.get('name'),
                    'postName': service_details_data.get('postName'),
                }
        
        return representation


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


# class JobRequestSerializer(serializers.ModelSerializer):
#     status = serializers.CharField(default='open')
#     class Meta:
#         model = JobRequest
#         fields ="__all__"
        # fields = ['id', 'title', 'description', 'location', 'budget', 'created_at', 'status', 'artisan']


# class CustomServiceCategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ServiceCategory
#         fields = ['name', 'postName']  # You can add other fields if needed




# class JobRequestSerializer(serializers.ModelSerializer):
#     service_details = CustomServiceCategorySerializer()  # Nested serializer for service_details

#     class Meta:
#         model = JobRequest
#         fields = "__all__"  # Default to include all fields

#     def to_representation(self, instance):
#         """
#         Modify the response based on the request method. For GET requests, include detailed service information.
#         """
#         representation = super().to_representation(instance)

#         # Check if the request is a GET request to include the detailed `service_details`
#         if self.context['request'].method == 'GET':
#             # We only want to include the name and postName for GET requests
#             representation['service_details'] = {
#                 'name': instance.service_details.name,
#                 'postName': instance.service_details.postName
#             }

#         return representation



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        # fields = ['job', 'customer', 'artisan', 'rating', 'comment', 'created_at']



from .models import JobRequest, Review, ServiceCategory
from rest_framework import serializers
from rest_framework import serializers
from .models import JobRequest, ServiceCategory
from users.models import CustomUser  # Ensure you import the CustomUser model

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['unique_id', 'first_name', 'last_name', 'email', 'phone']  # Include only the required fields

class ServiceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = "__all__"  # Return all fields for ServiceCategory



class JobRequestCreateSerializer(serializers.ModelSerializer):
    status = serializers.CharField(default='open')
    class Meta:
        model = JobRequest
        fields ="__all__"
        # fields = ['id', 'title', 'description', 'location', 'budget', 'created_at', 'status', 'artisan']


# class JobRequestSerializer(serializers.ModelSerializer):
#     status = serializers.CharField(default='open')
#     # service_details = serializers.PrimaryKeyRelatedField(queryset=ServiceCategory.objects.all())

#     service_details = ServiceCategorySerializer()  # Use ServiceCategorySerializer for nested serialization

#     class Meta:
#         model = JobRequest
#         fields = "__all__"  # Include all fields from JobRequest

#     def to_representation(self, instance):
#         """
#         Customize the representation of JobRequest to only return 'name' and 'postName' for the service_details field
#         during GET requests for JobRequest, without affecting the POST request format.
#         """
#         representation = super().to_representation(instance)
        
#         # Check if it's a GET request for JobRequest (not for ServiceCategory)
#         if self.context.get('request') and self.context['request'].method == 'GET':
#             customer = instance.customer
#             # Modify the service_details field to include only name and postName
#             service_details_data = representation.get('service_details', {})
#             if service_details_data:
#                 representation['service_details'] = {
#                     'name': service_details_data.get('name'),
#                     'postName': service_details_data.get('postName'),
#                 }
#             representation['customer'] = f"{customer.first_name} {customer.last_name}" if customer else None
        
#         return representation

class JobRequestSerializer(serializers.ModelSerializer):
    status = serializers.CharField(default='open')
    service_details = ServiceCategorySerializer(read_only=True)  # Nested serialization for service_details (read-only)
    artisan = CustomUserSerializer(read_only=True)  # Nested serialization for artisan (read-only)

    class Meta:
        model = JobRequest
        fields = "__all__"  # Include all fields from JobRequest

    def to_representation(self, instance):
        """
        Customize the representation of JobRequest to include nested artisan details.
        """
        representation = super().to_representation(instance)
        
        # Check if it's a GET request for JobRequest
        if self.context.get('request') and self.context['request'].method == 'GET':
            customer = instance.customer
            # Modify the service_details field to include only name and postName
            service_details_data = representation.get('service_details', {})
            if service_details_data:
                representation['service_details'] = {
                    'name': service_details_data.get('name'),
                    'postName': service_details_data.get('postName'),
                }
            representation['customer'] = f"{customer.first_name} {customer.last_name}" if customer else None
        
        return representation

    def update(self, instance, validated_data):
        """
        Handle updates to the JobRequest instance, including the artisan field.
        """
        # Handle the artisan field separately
        artisan_id = self.context['request'].data.get('artisan')
        if artisan_id:
            try:
                artisan = CustomUser.objects.get(unique_id=artisan_id)
                instance.artisan = artisan
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError({"artisan": "Artisan with the provided unique_id does not exist."})

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        # fields = ['job', 'customer', 'artisan', 'rating', 'comment', 'created_at']



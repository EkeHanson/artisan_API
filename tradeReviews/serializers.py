from rest_framework import serializers
from .models import TradeReview
from jobs.models import ServiceCategory
from users.models import CustomUser


class ServiceCategoryReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceCategory
        fields = ['name', 'postName']


class CustomerReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']


class TradeReviewsSerializer(serializers.ModelSerializer):
    # Use nested serializers for GET requests
    service_category = ServiceCategoryReadSerializer(read_only=True)
    customer = CustomerReadSerializer(read_only=True)

    # Use IDs for POST/PUT requests
    service_category_id = serializers.UUIDField(write_only=True)
    customer_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = TradeReview
        fields = "__all__"
        # fields = [
        #     'id', 'service_category', 'service_category_id',
        #     'customer', 'customer_id', 'reliability_rating',
        #     'workmanship_rating', 'tidiness_rating', 'courtesy_rating',
        #     'overall_rating', 'review_title', 'comment', 'value_of_work',
        #     'contact_name', 'contact_email', 'mobile_number', 'created_at'
        # ]

    def create(self, validated_data):
        # Extract IDs from validated data
        service_category_id = validated_data.pop('service_category_id')
        customer_id = validated_data.pop('customer_id')

        # Resolve instances from IDs
        service_category = ServiceCategory.objects.get(unique_id=service_category_id)
        customer = CustomUser.objects.get(unique_id=customer_id)

        # Create and return TradeReview instance
        return TradeReview.objects.create(
            service_category=service_category,
            customer=customer,
            **validated_data
        )

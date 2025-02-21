# Serializers
from rest_framework import serializers
from .models import SubscriptionPlan
# from users.models import CustomUser

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'
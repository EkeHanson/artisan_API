# serializers.py
from rest_framework import serializers
from .models import Payouts
from users.models import CustomUser

class PayoutsSerializer(serializers.ModelSerializer):
    artisan_unique_id = serializers.SlugRelatedField(
        queryset=CustomUser.objects.filter(user_type='artisan'),
        slug_field='unique_id',
        source='artisan'
    )

    class Meta:
        model = Payouts
        fields = ['artisan_unique_id', 'bank_name', 'account_number', 'account_name', 'account_type']
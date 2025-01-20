from rest_framework import serializers
from .models import QuoteRequest
from users.models import CustomUser

class QuoteRequestSerializer(serializers.ModelSerializer):
    quoting_customer = serializers.SlugRelatedField(
        queryset=CustomUser.objects.all(),
        slug_field='unique_id', write_only=True, required=False )

    class Meta:
        model = QuoteRequest
        fields = '__all__'

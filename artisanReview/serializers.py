from rest_framework import serializers
from .models import ArtisanReview
from users.models import CustomUser

class ArtisanReviewSerializer(serializers.ModelSerializer):
    reviewer_name = serializers.SerializerMethodField()

    class Meta:
        model = ArtisanReview
        fields = '__all__'

    def get_reviewer_name(self, obj):
        """
        Returns the first_name and last_name of the CustomUser linked to reviewer_name.
        """
        if obj.reviewer_name:
            return f"{obj.reviewer_name.first_name} {obj.reviewer_name.last_name}"
        return None

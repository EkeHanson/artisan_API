from rest_framework import serializers
from .models import ArtisanReview
from users.models import CustomUser

class ArtisanReviewSerializer(serializers.ModelSerializer):
    reviewer_name_display = serializers.SerializerMethodField(read_only=True)
    reviewer_name = serializers.SlugRelatedField(
        queryset=CustomUser.objects.all(),
        slug_field='unique_id',  # Use unique_id for lookups
        write_only=True
    )

    class Meta:
        model = ArtisanReview
        fields = '__all__'
        extra_kwargs = {
            'reviewer_name': {'write_only': True}  # Hide from GET responses
        }

    def get_reviewer_name_display(self, obj):
        """
        Returns the first_name and last_name of the CustomUser linked to reviewer_name.
        """
        if obj.reviewer_name:
            return f"{obj.reviewer_name.first_name} {obj.reviewer_name.last_name}"
        return None

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Payouts
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Payouts

class PayoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payouts
        fields = '__all__'

    def validate(self, data):
        """
        Ensure that each artisan can only have one Payouts instance when creating.
        Skip validation when updating an existing instance.
        """
        artisan = data.get('artisan')

        # Only enforce unique check when creating (self.instance is None)
        if self.instance is None and Payouts.objects.filter(artisan=artisan).exists():
            raise ValidationError("Each artisan can only have one Payouts instance.")

        return data

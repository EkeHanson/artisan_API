from rest_framework import serializers, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Payouts
from users.models import CustomUser

# Serializer
class PayoutsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payouts
        fields = '__all__'

    def validate(self, data):
        artisan = data.get('artisan')
        if Payouts.objects.filter(artisan=artisan).exists():
            raise ValidationError("Each artisan can only have one Payouts instance.")
        return data

# ViewSet
class PayoutsViewSet(viewsets.ModelViewSet):
    serializer_class = PayoutsSerializer
    permission_classes = [AllowAny]
    lookup_field = 'artisan__unique_id'  # Use unique_id instead of default id

    def get_queryset(self):
        return Payouts.objects.all()

    def retrieve(self, request, artisan__unique_id=None):
        queryset = self.get_queryset()
        payout = get_object_or_404(queryset, artisan__unique_id=artisan__unique_id)
        serializer = self.get_serializer(payout)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        artisan = request.data.get("artisan")
        if Payouts.objects.filter(artisan=artisan).exists():
            return Response({"error": "Each artisan can only have one Payouts instance."}, status=400)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        artisan__unique_id = kwargs.get('artisan__unique_id')
        queryset = self.get_queryset()
        payout = get_object_or_404(queryset, artisan__unique_id=artisan__unique_id)
        
        partial = kwargs.get('partial', False)  # Fix: Handle partial updates correctly
        serializer = self.get_serializer(payout, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, artisan__unique_id=None):
        queryset = self.get_queryset()
        payout = get_object_or_404(queryset, artisan__unique_id=artisan__unique_id)
        payout.delete()
        return Response({'message': 'Payout deleted successfully'}, status=204)

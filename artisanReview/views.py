

from rest_framework.viewsets import ModelViewSet
from .models import ArtisanReview
from .serializers import ArtisanReviewSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
import logging

# Configure logging
logger = logging.getLogger(__name__)

class TradeReviewViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = ArtisanReview.objects.all().order_by('id')
    serializer_class = ArtisanReviewSerializer

    def get_serializer_context(self):
        """
        Include the request in the serializer context.
        """
        return {'request': self.request}

    def create(self, request, *args, **kwargs):
        """
        Handle POST requests and log errors if validation fails.
        """
        serializer = self.get_serializer(data=request.data)

        print("request.data")
        print(request.data)
        print("request.data")
        if not serializer.is_valid():
            # Log the serializer errors
            #logger.error(f"POST request validation errors: {serializer.errors}")
            print(f"POST request validation errors: {serializer.errors}")  # Optional console output
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Handle PUT requests and log errors if validation fails.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            # Log the serializer errors
            logger.error(f"PUT request validation errors: {serializer.errors}")
            print(f"PUT request validation errors: {serializer.errors}")  # Optional console output
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='artisan/(?P<artisan_id>[^/.]+)')
    def get_reviews_for_artisan(self, request, artisan_id=None):
        """
        Retrieve all reviews for a specific artisan.
        """
        reviews = ArtisanReview.objects.filter(artisan=artisan_id)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

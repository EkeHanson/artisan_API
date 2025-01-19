from rest_framework.viewsets import ModelViewSet
from .models import TradeReview
from .serializers import TradeReviewsSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


class TradeReviewViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = TradeReview.objects.all().order_by('id')
    serializer_class = TradeReviewsSerializer

    def create(self, request, *args, **kwargs):
        """Handle POST requests with detailed error logging."""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # Log and print the errors
            error_message = f"POST request errors: {serializer.errors}"
            print(error_message)  # Print to console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        """Handle PATCH requests with detailed error logging."""
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            # Log and print the errors
            error_message = f"PATCH request errors: {serializer.errors}"
            #print(error_message)  # Print to console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
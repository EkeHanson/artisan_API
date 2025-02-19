from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import QuoteRequest
from .serializers import QuoteRequestSerializer
from users.models import CustomUser
from jobs.models import JobRequest

class QuotationViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = QuoteRequest.objects.all().order_by('-id')
    serializer_class = QuoteRequestSerializer

    def create(self, request, *args, **kwargs):

        artisan_id = request.data.get("artisan_id")
        job_id = request.data.get("job_request_id")

        if not artisan_id or not job_id:
            return Response(
                {"error": "Both artisan_id and job_request_id are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if artisan exists and is valid
        try:
            artisan = CustomUser.objects.get(unique_id=artisan_id, user_type="artisan")
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Invalid artisan_id. No artisan found with this ID."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the job exists
        try:
            job = JobRequest.objects.get(unique_id=job_id)
        except JobRequest.DoesNotExist:
            return Response(
                {"error": "Invalid job_request_id. No job found with this ID."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the artisan has already submitted a quote for this job
        if QuoteRequest.objects.filter(artisan=artisan, job_request=job).exists():
            return Response(
                {"error": "You have already submitted a quote for this job."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Serialize and validate the request data
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid data provided.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save the quote request
        try:
            serializer.save(artisan=artisan, job_request=job)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred while saving the quote.", "details": str(e)}
                ,status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(
                {"error": "Invalid data provided.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ["create", "list", "destroy"]:
            return [AllowAny()]
        return [AllowAny()]

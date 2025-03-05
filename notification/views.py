from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Notofication
from .serializers import NotoficationRequestSerializer
from users.models import CustomUser
from jobs.models import JobRequest
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Notofication
from .serializers import NotoficationRequestSerializer
from users.models import CustomUser
from jobs.models import JobRequest
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination


class NotoficationViewSetPagination(PageNumberPagination):
    page_size = 15  # Default number of items per page
    page_size_query_param = 'page_size'  # Allow client to override, e.g., ?page_size=20
    max_page_size = 100  # Maximum allowed page size


class NotoficationViewSet(ModelViewSet):
    permission_classes = [AllowAny]
   # queryset = Notofication.objects.all().order_by('-id')
    queryset = Notofication.objects.all().order_by('created_at')
    serializer_class = NotoficationRequestSerializer
    pagination_class = NotoficationViewSetPagination  # Use the custom pagination class
    lookup_field = "unique_id"  # ✅ Ensure DRF matches unique_id instead of id (pk)

    def get(self, request, *args, **kwargs):
        unique_id = request.query_params.get('unique_id')
        if not unique_id:
            return Response({"error": "unique_id query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)

        notofication = Notofication.objects.filter(unique_id=unique_id)

        if not notofication.exists():
            raise NotFound({"error": "Notofication with this unique_id does not exist."})

      
        serializer = NotoficationRequestSerializer(notofication.first())
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        # print("request.data.get")
        # print(request.data)
        # print("request.data.get")

        artisan_id = request.data.get("artisan_id")
        customer_id = request.data.get("customer_id")
        job_request_id = request.data.get("job_request_id")

        # print("request.data.get")
        # print(artisan_id)
        # print(customer_id)
        # print(job_request_id)
        # print("request.data.get")

        # if not artisan_id or not job_request_id or not customer_id:
        #     return Response(
        #         {"error": "artisan_id, customer_id, and job_request_id are required."},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # Check if customer exists
        try:
            customer = CustomUser.objects.get(unique_id=customer_id, user_type="customer")
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Invalid customer_id. No customer found with this ID."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # print("request.data.get")
        # print(artisan_id)
        # print(customer_id)
        # print(job_request_id)
        # print("request.data.get")
     
        try:
            print("request.data.get")
            print(artisan_id)
            print("request.data.get")

            artisan = CustomUser.objects.get(unique_id=artisan_id, user_type="artisan")
            print("request.data.get")
            print(artisan)
            print("request.data.get")
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Invalid artisan_id. No artisan found with this ID."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        print("request.data.get")
        print(artisan)
        print("request.data.get")

        # Check if job request exists
        try:
            job = JobRequest.objects.get(unique_id=job_request_id)
        except JobRequest.DoesNotExist:
            return Response(
                {"error": "Invalid job_request_id. No job found with this ID."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        print("job")
        print(job)
        print("job")

        # Proceed with creating the notification
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
     
        else:
            print("serializer.errors")
            print(serializer.errors)
            print("serializer.errors")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

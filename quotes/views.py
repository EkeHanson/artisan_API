from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import QuoteRequest, Booking
from .serializers import QuoteRequestSerializer, BookingSerializer
from users.models import CustomUser
from jobs.models import JobRequest
from rest_framework.decorators import action
from .serializers import CustomUserSerializer 
from notification.models import  Notofication
from payments.models import Payment
from django.shortcuts import get_object_or_404

class QuotationViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = QuoteRequest.objects.all().order_by('-id')
    serializer_class = QuoteRequestSerializer
    lookup_field = "unique_id"  # ✅ Ensure DRF matches unique_id instead of id (pk)

 
    # @action(detail=False, methods=["get"], url_path="artisan-bookings")
    # def artisan_bookings(self, request):
    #     """
    #     Returns all bookings for a particular artisan along with complete quote data.
    #     """
    #     artisan_id = request.query_params.get("artisan_id")
        
    #     if not artisan_id:
    #         return Response({"error": "artisan_id is required."}, status=status.HTTP_400_BAD_REQUEST)

    #     bookings = Booking.objects.filter(artisan__unique_id=artisan_id).select_related("quote", "artisan", "job_request")
        
    #     if not bookings.exists():
    #         return Response({"error": "You do not have any bookings yet."}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = BookingSerializer(bookings, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"], url_path="artisan-bookings")
    def artisan_bookings(self, request):
        """
        Returns all bookings for a particular artisan along with complete quote data.
        """
        artisan_id = request.query_params.get("artisan_id")

        if not artisan_id:
            return Response({"error": "artisan_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        bookings = Booking.objects.filter(artisan__unique_id=artisan_id).select_related("quote", "artisan", "job_request")

        if not bookings.exists():
            return Response({"error": "You do not have any bookings yet."}, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



    @action(detail=True, methods=["post"], url_path="accept_quote_via_artisan")
    def accept_quote_via_artisan(self, request, unique_id=None):  # ✅ Use unique_id instead of pk
        """
        Accepts a quote and creates a booking for it.
        """
  
        try:
            quote = QuoteRequest.objects.get(unique_id=unique_id)  # ✅ Ensure lookup uses unique_id
            customer = quote.job_request.customer  # ✅ Directly assign the customer instance
            if not isinstance(customer, CustomUser):  # Safety check
                return Response({"error": "Invalid customer reference"}, status=status.HTTP_400_BAD_REQUEST)
        except QuoteRequest.DoesNotExist:
            return Response({"error": "Quote not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # Check if booking already exists
        if Booking.objects.filter(quote=quote).exists():
            return Response({"error": "This quote has already been accepted"}, status=status.HTTP_400_BAD_REQUEST)

        # Get payment reference from request
        payment_reference = request.data.get("payment_reference")

        # Fetch payment details
        payment = get_object_or_404(Payment, reference=payment_reference, user=customer)

        if payment.status != "success":
            return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new booking     
        booking = Booking.objects.create(
            quote=quote,
            customer=quote.job_request.customer,
            artisan=quote.artisan,
            job_request=quote.job_request,
        )
        
        # self.create_notification_for_job(quote.artisan, customer, quote,quote.job_request)

        Notofication.objects.create(
        artisan=quote.artisan,
        customer=customer,
        notification_message=f" {customer.first_name} {customer.last_name} has successfully paid {quote.bid_amount} to {quote.artisan.first_name} {quote.artisan.last_name} for {quote.job_request.title} job which is supposed to be completed at {quote.job_request.location} in {quote.job_duration}.",
        notification_type="payment_made"
        )

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
    

    @action(detail=True, methods=["post"], url_path="accept_quote_via_escrow")
    def accept_quote_via_escrow(self, request, unique_id=None):  # ✅ Use unique_id instead of pk
        """
        Accepts a quote and creates a booking for it.
        """
  
        try:
            quote = QuoteRequest.objects.get(unique_id=unique_id)  # ✅ Ensure lookup uses unique_id
            customer = quote.job_request.customer  # ✅ Directly assign the customer instance
            if not isinstance(customer, CustomUser):  # Safety check
                return Response({"error": "Invalid customer reference"}, status=status.HTTP_400_BAD_REQUEST)
        except QuoteRequest.DoesNotExist:
            return Response({"error": "Quote not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # Check if booking already exists
        if Booking.objects.filter(quote=quote).exists():
            return Response({"error": "This quote has already been accepted"}, status=status.HTTP_400_BAD_REQUEST)

        # Get payment reference from request
        payment_reference = request.data.get("payment_reference")

        # Fetch payment details
        payment = get_object_or_404(Payment, reference=payment_reference, user=customer)

        if payment.status != "success":
            return Response({"error": "Payment verification failed"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new booking     
        booking = Booking.objects.create(
            quote=quote,
            customer=quote.job_request.customer,
            artisan=quote.artisan,
            job_request=quote.job_request,
        )
        
        # self.create_notification_for_job(quote.artisan, customer, quote,quote.job_request)
        
        Notofication.objects.create(
        artisan=quote.artisan,
        customer=customer,
        notification_message=f" {customer.first_name} {customer.last_name} has successfully paid  {quote.bid_amount} to the SimserviceHub Escrow Account.",
        notification_type="payment_made"
        )

        return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
    

    @action(detail=False, methods=["get"], url_path="artisans-for-job")
    def artisans_for_job(self, request):
        job_id = request.query_params.get("job_id")

        if not job_id:
            return Response({"error": "job_id is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            job = JobRequest.objects.get(unique_id=job_id)
        except JobRequest.DoesNotExist:
            return Response({"error": "Invalid job_id. No job found."}, status=status.HTTP_400_BAD_REQUEST)

        quotes = QuoteRequest.objects.filter(job_request=job).select_related("artisan")

        # Avoid duplicate artisan information by removing redundant data
        response_data = [
            {
                "artisan": {
                    **CustomUserSerializer(quote.artisan).data,
                    # "about_artisan": quote.artisan.about_artisan.split("\n\n")[0],  # Remove duplicate paragraphs
                },
                "quote": QuoteRequestSerializer(quote).data,
            }
            for quote in quotes
        ]

        return Response(response_data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):

        # print("request.data")
        # print(request.data)
        # print("request.data")

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

            # print("serializer.errors")
            # print(serializer.errors)
            # print("serializer.errors")
            return Response(
                {"error": "Invalid data provided.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save the quote request and update job.num_appllications
        try:
            quote_data  = serializer.save(artisan=artisan, job_request=job)


            job.num_appllications += 1
            job.save(update_fields=["num_appllications"])

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": "An unexpected error occurred while saving the quote.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    # def create_notification_for_job(self, artisan, customer, quote, job_request):
    #     """
    #     Create a notification when a job is created.

    #     print
    #     """
        
    #     try:         
    #         Notofication.objects.create(
    #         artisan=artisan,
    #         customer=customer,
    #         notification_message=f" {customer.first_name} {customer.last_name} has successfully paid  {quote.bid_amount} to the SimserviceHub Escrow Account.",
    #         notification_type="payment_made"
    #     )
           
    #     except Exception as e:
    #         print(f"Error creating notification: {e}")


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



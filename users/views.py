from .models import CustomUser
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer, ResetPasswordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status, generics, viewsets, views
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from django.core.files.base import ContentFile
from twilio.rest import Client
import random
from django.core.cache import cache
from django.conf import settings
from django.shortcuts import get_object_or_404


class SendLoginTokenView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        phone_number = request.data.get('phone')

        # print("request.data")
        # print(request.data)
        # print("request.data")

        if not email and not phone_number:
            return Response({'error': 'Either email or phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        if email:
            user = CustomUser.objects.filter(email=email).first()
        elif phone_number:
            user = CustomUser.objects.filter(phone=phone_number).first()

        if not user:
            return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

        token = random.randint(10000, 99999)
        cache_key = f'login_token_{email or phone_number}'
        cache.set(cache_key, token, timeout=300)

        # print("token=data")
        # print(token)
        # print("token=data")

        sms_message_body = f'Your login token is {token}. It is valid for 5 minutes.'
        email_message_body = f'''
            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Simservicehub Email Verification Token</title>
            </head>
            <body style="margin: 0; padding: 0; font-family: Poppins, sans-serif; font-size: 15px; font-weight: 400; line-height: 1.5; width: 100%; background: #3B4B11; color: #FB9836; overflow-x: hidden; min-height: 100vh; text-align: center;">
                <div style="position: relative; width: 100%; height: auto; min-height: 100%; display: flex; justify-content: center;">
                    <div style="position: relative; width: 700px; height: auto; text-align: center; padding: 80px 0px; padding-bottom: 0px !important;">
                        <img src="https://www.simservicehub.com/assets/site-logo-marnjd0k.png" style="max-width: 150px; margin-bottom: 80px;" />
                        <h3 style="font-size: 30px; font-weight: 700;">Your login token is: {token}.</h3>
                        <h3 style="font-size: 30px; font-weight: 700;">Please Note that this token is only valid for 5 minutes.</h3>
                        <footer style="position: relative; width: 100%; height: auto; margin-top: 50px; padding: 30px; background-color: rgba(255,255,255,0.1);">
                            <h5>Thanks for using our platform</h5>
                            <p style="font-size: 13px !important; color: #fff !important;">You can reach us via <a href="mailto:support@simservicehub.com" style="color:#D8F3DC !important; text-decoration: underline !important;">support@simservicehub.com</a></p>
                            <p style="font-size: 13px !important; color: #fff !important;">© <script>document.write(new Date().getFullYear());</script> Simservicehub. All rights reserved.</p>
                        </footer>
                    </div>
                </div>
            </body>
            </html>

            '''

        if email:
            send_mail(
                'Your Login Token',
                email_message_body,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
                html_message=email_message_body,
            )
            return Response({'message': 'Login token has been sent to your email'}, status=status.HTTP_200_OK)
        elif phone_number:
            try:
                # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                client = Client('AC500ccdccd6ebc368dc82d8e36731e000', 'ba57440dbf551131d0eb006dd9fdedc2')
                client.messages.create(
                    from_='+15074426880',
                    # from_=settings.TWILIO_PHONE_NUMBER,
                    body=sms_message_body,
                    to=phone_number
                )
                return Response({'message': 'Login token has been sent via SMS'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyLoginTokenView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        identifier = request.data.get('email') or request.data.get('phone')
        token = request.data.get('token')

        if not identifier or not token:
            return Response({'error': 'Identifier (email or phone) and token are required'}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f'login_token_{identifier}'
        cached_token = cache.get(cache_key)

        if str(cached_token) == str(token):
            user = CustomUser.objects.filter(email=identifier).first() or CustomUser.objects.filter(phone=identifier).first()

            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'userId': user.id,
                    'unique_user_id': user.unique_id,
                    'user_type': user.user_type,
                    'user_date_joined': user.date_joined,
                    'email': user.email,
                    'address': user.address,
                    'user_type': user.user_type,
                    'phone': user.phone,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)



class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-id')
    serializer_class = UserSerializer
    lookup_field = "unique_id"  # Ensures that DRF uses unique_id for lookups

    def create(self, request, *args, **kwargs):
        """Handle POST requests with detailed error logging."""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            # Log and print the errors
            error_message = f"POST request errors: {serializer.errors}"
            print(error_message)  # Print to console
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        # print("serializer.data")
        # print(serializer.data)
        # print("serializer.data")
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get_object(self):
        """Retrieve the user object using `unique_id` instead of `pk`."""
        unique_id = self.kwargs.get("unique_id")
        return get_object_or_404(CustomUser, unique_id=unique_id)

    def partial_update(self, request, *args, **kwargs):
        """Update user details using unique_id instead of pk."""

        # print("request.data")
        # print(request.data)
        # print("request.data")
        user = self.get_object()  # Uses `get_object()` to fetch by `unique_id`
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        # print("serializer.errors")
        # print(serializer.errors)
        # print("serializer.errors")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        # For 'create' and 'list' actions, allow anyone
        if self.action in ['create', 'list']:
            return [AllowAny()]
        # For 'delete' action, allow anyone (no authentication required)
        elif self.action == 'destroy':
            return [AllowAny()]
        # For all other actions, require authentication
        #return [IsAuthenticated()]
        return [AllowAny()]




    def get_permissions(self):
        # For 'create' and 'list' actions, allow anyone
        if self.action in ['create', 'list']:
            return [AllowAny()]
        # For 'delete' action, allow anyone (no authentication required)
        elif self.action == 'destroy':
            return [AllowAny()]
        # For all other actions, require authentication
        #return [IsAuthenticated()]
        return [AllowAny()]


class LoginView(generics.GenericAPIView): 
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'email': user.email,
                'userId': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_joined': user.date_joined,
            }, status=status.HTTP_200_OK)

        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class ResetPasswordView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Generate reset token and UID
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"https://www.simservicehub.com/forgotten_pass_reset/{uid}/{token}/"

        # Prepare email content
        subject = 'Password Reset Request'

        # Use a proper HTML template for the message
        message = f"Please click the following link to reset your password: {reset_link}"
        html_message = f'''


            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>CMVP Registration Email Verification </title>
            </head>
            <body style="margin: 0; padding: 0; font-family: Poppins, sans-serif; font-size: 15px; font-weight: 400; line-height: 1.5; width: 100%; background: #3B4B11; color: #FB9836; overflow-x: hidden; min-height: 100vh; text-align: center;">
                <div style="position: relative; width: 100%; height: auto; min-height: 100%; display: flex; justify-content: center;">
                    <div style="position: relative; width: 700px; height: auto; text-align: center; padding: 80px 0px; padding-bottom: 0px !important;">
                        <img src="https://www.simservicehub.com/assets/site-logo-marnjd0k.png" style="max-width: 150px; margin-bottom: 80px;" />
                        <h3 style="font-size: 30px; font-weight: 700;">Please click on the link below to reset your password!</h3>
                        <p style="margin-top: 10px; color:#D8F3DC;"><a href="{reset_link}"><strong>Reset Password</strong></p><p style="margin-top: 10px; color:#D8F3DC;">Note this email will expire in five (5) minutes.</p>

                        <footer style="position: relative; width: 100%; height: auto; margin-top: 50px; padding: 30px; background-color: rgba(255,255,255,0.1);">
                            <h5>Thanks for using our platform</h5>
                            <p style="font-size: 13px !important; color: #fff !important;">You can reach us via <a href="mailto:support@simservicehub.com" style="color:#D8F3DC !important; text-decoration: underline !important;">support@simservicehub.com</a></p>
                            <p style="font-size: 13px !important; color: #fff !important;">© <script>document.write(new Date().getFullYear());</script> Simservicehub. All rights reserved.</p>
                        </footer>
                    </div>
                </div>
            </body>
            </html>

        '''

        from_email =  settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        # Send the email with the HTML content
        send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=html_message)

        return Response({'message': 'Password reset link has been sent to your email'}, status=status.HTTP_200_OK)


class ConfirmResetPasswordView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token, *args, **kwargs):

        serializer = ResetPasswordSerializer(data=request.data)

        # Validate the serializer
        if not serializer.is_valid():
            # print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            # Token is valid; proceed with password reset
            new_password = serializer.validated_data['new_password']
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_contact_email(request):
    if request.method == 'POST':
        email = request.data.get('email')
        full_name = request.data.get('fullName')
        phone_number = request.data.get('phone')
        interest_service = request.data.get('serviceInterest')
        message_body = request.data.get('message')

        if email:
            subject = 'Contact Form Submission'
            message = f'''

            <html>
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>CMVP Registration Email Verification </title>
            </head>
            <body style="margin: 0; padding: 0; font-family: Poppins, sans-serif; font-size: 15px; font-weight: 400; line-height: 1.5; width: 100%; background: #3B4B11; color: #FB9836; overflow-x: hidden; min-height: 100vh; text-align: center;">
                <div style="position: relative; width: 100%; height: auto; min-height: 100%; display: flex; justify-content: center;">
                    <div style="position: relative; width: 700px; height: auto; text-align: center; padding: 80px 0px; padding-bottom: 0px !important;">
                        <img src="https://www.simservicehub.com/assets/site-logo-marnjd0k.png" style="max-width: 150px; margin-bottom: 80px;" />
                        <h3 style="font-size: 30px; font-weight: 700;">Contact Form Submission</h3>
                        <p style="margin-top: 10px; color:#D8F3DC;"><strong>Full Name:</strong> {full_name}</p>
                        <p style="margin-top: 10px; color:#D8F3DC;">Email Address:</strong> {email}</p>
                        <p style="margin-top: 10px; color:#D8F3DC;">Phone Number:</strong> {phone_number}</p>
                        <p style="margin-top: 10px; color:#D8F3DC;">Interest Service:</strong> {interest_service}</p>
                        <p style="margin-top: 10px; color:#D8F3DC;">Message:</strong> {message_body}</p>

                        <footer style="position: relative; width: 100%; height: auto; margin-top: 50px; padding: 30px; background-color: rgba(255,255,255,0.1);">
                            <h5>Thanks for using our platform</h5>
                            <p style="font-size: 13px !important; color: #fff !important;">You can reach us via <a href="mailto:support@simservicehub.com" style="color:#D8F3DC !important; text-decoration: underline !important;">support@simservicehub.com</a></p>
                            <p style="font-size: 13px !important; color: #fff !important;">© <script>document.write(new Date().getFullYear());</script> Simservicehub. All rights reserved.</p>
                        </footer>
                    </div>
                </div>
            </body>
            </html>

            '''
            recipient_list = ['ekehanson@gmail.com']

            from_email = settings.DEFAULT_FROM_EMAIL

            send_mail(subject, '', from_email, recipient_list, fail_silently=False, html_message=message)
            return Response({'message': 'Email sent successfully'})
        else:
            return Response({'error': 'Email not provided in POST data'}, status=400)
    else:
        return Response({'error': 'Invalid request method'}, status=400)

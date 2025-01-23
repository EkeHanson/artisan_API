from .models import CustomUser
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

        message_body = f'Your login token is {token}. It is valid for 5 minutes.'

        if email:
            send_mail(
                'Your Login Token',
                message_body,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False
            )
            return Response({'message': 'Login token has been sent to your email'}, status=status.HTTP_200_OK)
        elif phone_number:
            try:
                # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                client = Client('AC500ccdccd6ebc368dc82d8e36731e000', 'ba57440dbf551131d0eb006dd9fdedc2')
                client.messages.create(
                    from_='+15074426880',
                    # from_=settings.TWILIO_PHONE_NUMBER,
                    body=message_body,
                    to=phone_number
                )
                return Response({'message': 'Login token has been sent via SMS'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class SendLoginTokenView(views.APIView):
#     permission_classes = [AllowAny]

#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         phone_number = request.data.get('phone')

#         if not email and not phone_number:
#             return Response({'error': 'Either email or phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

#         if email:
#             user = CustomUser.objects.filter(email=email).first()
#         elif phone_number:
#             user = CustomUser.objects.filter(phone=phone_number).first()

#         if not user:
#             return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

#         token = random.randint(10000, 99999)
#         cache_key = f'login_token_{email or phone_number}'
#         cache.set(cache_key, token, timeout=300)

#         message_body = f'Your login token is {token}. It is valid for 5 minutes.'

#         if email:
#             send_mail(
#                 'Your Login Token',
#                 message_body,
#                 settings.DEFAULT_FROM_EMAIL,
#                 [email],
#                 fail_silently=False
#             )
#             return Response({'message': 'Login token has been sent to your email'}, status=status.HTTP_200_OK)
#         elif phone_number:
#             try:

#                 #DEFAULT_account_sid = 'AC500ccdccd6ebc368dc82d8e36731e000'  # Your Twilio Account SID
#                 # DEFAULT_auth_token = 'cc78f85b4552f9c448fcfbac0226b72c'

#                 DEFAULT_account_sid = 'AC78c683b23aae439dc578e492597cd40e'  # Your Twilio Account SID
#                 DEFAULT_auth_token = '39d70a911f789435ac3554dfccd066b2' 
#                 TWILIO_PHONE_NUMBER = '+15074426880'
#                 client = Client(DEFAULT_account_sid, DEFAULT_auth_token)
#                 client.messages.create(
#                     from_=TWILIO_PHONE_NUMBER,
#                     body=message_body,
#                     to=phone_number
#                 )
#                 return Response({'message': 'Login token has been sent via SMS'}, status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
                    'email': user.email,
                    'user_type': user.user_type,
                    'phone': user.phone,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }, status=status.HTTP_200_OK)
        
        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('-id')
    serializer_class = UserSerializer

    
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
        reset_link = f"https://swiftlookv1.vercel.app/forgotten_pass_reset/{uid}/{token}/"

        # Prepare email content
        subject = 'Password Reset Request'

        # Use a proper HTML template for the message
        message = f"Please click the following link to reset your password: {reset_link}"
        html_message = f'''
            <html>
                <body>
                    <h3>Please click on the link below to reset your password</h3>
                    <p><a href="{reset_link}"><strong>Reset Password</strong></a></p>
                    <p> Note this email will expire in five (5) minutes. </p>
                </body>
            </html>
        '''

        from_email = 'ekenehanson@sterlingspecialisthospitals.com'
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
            <body>
                <h3>Contact Form Submission</h3>
                <p><strong>Full Name:</strong> {full_name}</p>
                <p><strong>Email Address:</strong> {email}</p>
                <p><strong>Phone Number:</strong> {phone_number}</p>
                <p><strong>Interest Service:</strong> {interest_service}</p>
                <p><strong>Message:</strong> {message_body}</p>
            </body>
            </html>
            '''
            recipient_list = [email]

            from_email = settings.DEFAULT_FROM_EMAIL

            send_mail(subject, '', from_email, recipient_list, fail_silently=False, html_message=message)
            return Response({'message': 'Email sent successfully'})
        else:
            return Response({'error': 'Email not provided in POST data'}, status=400)
    else:
        return Response({'error': 'Invalid request method'}, status=400)

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

import random
from django.core.cache import cache

class SendLoginTokenView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)

        except CustomUser.DoesNotExist:
            
            return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

        # Generate a 5-digit token
        token = random.randint(10000, 99999)

        # Store token in cache or any secure storage with a short expiration time (e.g., 5 minutes)
        cache.set(f'login_token_{email}', token, timeout=300)

        # Send the token to the user's email
        subject = 'Your Login Token'
        message = f'Your login token is {token}. It is valid for 5 minutes.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return Response({'message': 'Login token has been sent to your email'}, status=status.HTTP_200_OK)


class VerifyLoginTokenView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        token = request.data.get('token')

        if not email or not token:
            return Response({'error': 'Email and token are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve the token from cache
        cached_token = cache.get(f'login_token_{email}')

        if str(cached_token) == str(token):
            # Token is valid; proceed with the next step, e.g., generating JWT tokens
            user = CustomUser.objects.get(email=email)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),

                'email': user.email,
                'phone': user.phone,
                'address': user.address,
                
                'userId': user.id,
                'user_type': user.user_type,
                
                'userUnique_id': user.unique_id,
                'first_name': user.first_name,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_joined': user.date_joined,
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all().order_by('id')
    serializer_class = UserSerializer

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

        
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all().order_by('id') 
#     serializer_class = UserSerializer
#     permission_classes = [AllowAny]
    

#     def get_permissions(self):
#         if self.action in ['create', 'list']:
#             return [AllowAny()]
#         return [IsAuthenticated()]


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


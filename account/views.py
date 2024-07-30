# Create your views here.

from django.contrib.auth import get_user_model
from passlib.context import CryptContext
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from account.serializers import (UserLoginSerializer, ConfirmationCodeSerializer,

                                 UserListSerializer, UserSerializer, \
                                 PasswordResetRequestSerializer,
                                 PasswordResetCodeSerializer, PasswordChangeSerializer)
from .serializers import UserCreateSerializer, UserUpdateSerializer

User = get_user_model()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

from django.core.cache import cache

import random
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from passlib.context import CryptContext
from account.tasks import send_password_reset_email
User = get_user_model()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class RegisterAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny,]

    def generate_confirmation_code(self):
        return random.randrange(10000, 99999)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        # username = serializer.validated_data['username']

        confirmation_code = self.generate_confirmation_code()

        # Send confirmation email
        subject = 'Registration Confirmation Code'
        message = f'Your confirmation code is: {confirmation_code}'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)

        # Save the data in session
        request.session['registration_data'] = {
            'email': email,
            'password': password,
            'confirmation_code': confirmation_code
        }

        return Response({'confirmation_code': confirmation_code}, status=status.HTTP_201_CREATED)


class ConfirmationCodeAPIView(GenericAPIView):
    serializer_class = ConfirmationCodeSerializer
    permission_classes = [AllowAny,]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        confirm_code = request.data.get('confirm_code')
        registration_data = request.session.get('registration_data')
        print(registration_data.get('email'))
        print(registration_data.get('confirmation_code'))

        if not registration_data or registration_data.get('email') != email:
            return Response({'message': 'Invalid or expired confirmation code!'}, status=status.HTTP_400_BAD_REQUEST)

        if confirm_code == registration_data['confirmation_code']:
            password = registration_data['password']

            if User.objects.filter(email=email).exists():
                return Response({'success': False, 'message': 'This email already exists!'}, status=400)
            else:
                user = User.objects.create_user(
                    email=email,
                    password=password,
                )
                del request.session['registration_data']
                return Response({'success': True})
        else:
            return Response({'message': 'The entered code is not valid!'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def generate_confirmation_code(self):
        return random.randrange(10000, 99999)

    def post(self, request, send_password_reset_email=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            reset_code = self.generate_confirmation_code()
            request.session['reset_code'] = reset_code
            request.session['reset_email'] = email

            subject = 'Password Reset Request'
            message = f'Your password reset code is: {reset_code}'

            # Call the Celery task to send the email
            send_password_reset_email.delay(subject, message, [email])

            return Response({'success': 'Password reset code sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetWithCodeView(GenericAPIView):
    serializer_class = PasswordResetCodeSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            code = serializer.validated_data.get('code')

            session_code = request.session.get('reset_code')
            session_email = request.session.get('reset_email')
            print(session_code,session_email)
            if session_code is not None and session_email == email and str(session_code) == code:
                request.session['reset_verified'] = True
                return Response({'success': 'Code successfully checked'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid code or code has expired'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(GenericAPIView):
    serializer_class = PasswordChangeSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            new_password = serializer.validated_data['new_password']
            reset_verified = request.session.get('reset_verified', False)

            if reset_verified and request.session.get('reset_email') == email:
                try:
                    user = User.objects.get(email=email)
                    user.set_password(new_password)
                    user.save()

                    # Clear session data after successful password change
                    del request.session['reset_code']
                    del request.session['reset_email']
                    del request.session['reset_verified']

                    return Response({'success': 'Password changed successfully'}, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"error": "Invalid code or code has expired"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserList(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    queryset = User.objects.all().order_by('id')

    serializer_class = UserListSerializer


class CustomAuthToken(ObtainAuthToken):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email  # Return user's email instead of username
        })

class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return self.request.user  # Get the current user

    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)  # Allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)

class UserInfo(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)
    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response(user_serializer.data)
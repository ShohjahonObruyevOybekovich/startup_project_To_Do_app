# Create your views here.
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from passlib.context import CryptContext
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from account.serializers import (UserLoginSerializer, ConfirmationCodeSerializer,

                                 UserListSerializer, UserSerializer, \
                                 PasswordResetRequestSerializer,
                                 PasswordResetCodeSerializer)
from .serializers import UserCreateSerializer, UserUpdateSerializer

User = get_user_model()
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class RegisterAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer

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

        cache_data = {
            'email': email,
            # 'username': username,
            'password': password,
            'confirmation_code': confirmation_code
        }
        # print(cache_data)
        cache.set(email, cache_data, timeout=300)
        # print(cache)
        return Response({'confirmation_code': confirmation_code}, status=status.HTTP_201_CREATED)


class ConfirmationCodeAPIView(GenericAPIView):
    serializer_class = ConfirmationCodeSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        # username = request.data.get('username')
        confirm_code = request.data.get('confirm_code')
        cached_data = cache.get(email)

        print(confirm_code)
        print(cached_data)
        if confirm_code == cached_data['confirmation_code']:
            password = cached_data['password']

            if User.objects.filter(email=email).exists():
                return Response({'success': False, 'message': 'This email already exists!'}, status=400)
            # if User.objects.filter(username=cached_data['username']).exists():
            #     return Response({'success': False, 'message': 'This username already exists!'}, status=400)
            else:
                User.objects.create_user(
                    email=email,
                    # username=cached_data['username'],
                    password=password,
                )
                return Response({'success': True})
        else:
            return Response({'message': 'The entered code is not valid! '}, status=status.HTTP_400_BAD_REQUEST)



class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    def generate_confirmation_code(self):
        return random.randrange(10000, 99999)
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            reset_code = self.generate_confirmation_code()
            cache.set(email,reset_code, timeout=300)
            subject = 'Password Reset Request'
            message = f'Your password reset code is: {reset_code}'

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)

            return Response({'success': 'Password reset code sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class PasswordResetWithCodeView(GenericAPIView):
    serializer_class = PasswordResetCodeSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = cache.get('reset_code')
            print(code)
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'Invalid code or code has expired'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({'success': 'Password reset successfully'}, status=status.HTTP_200_OK)
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
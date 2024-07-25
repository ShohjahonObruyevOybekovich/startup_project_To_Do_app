
from django.urls import path

from .views import (CustomAuthToken,
                    UserUpdateAPIView, LogoutAPIView, RegisterAPIView, ConfirmationCodeAPIView,
                    UserList, UserInfo, PasswordResetRequestView, PasswordResetWithCodeView, )

urlpatterns = [
    path('token/', CustomAuthToken.as_view(), name='user_login'),

    path('create/', RegisterAPIView.as_view(), name='user_create'),
    path('confirm-code/', ConfirmationCodeAPIView.as_view(), name='confirm_code'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset/', PasswordResetWithCodeView.as_view(), name='password_reset_with_code'),

    path('user-list/',UserList.as_view(), name='user_list'),
    path('user-update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('user-info/',UserInfo.as_view(), name='user-info')
]
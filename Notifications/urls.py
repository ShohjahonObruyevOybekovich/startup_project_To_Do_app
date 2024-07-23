from django.urls import path, re_path
from . import consumers

urlpatterns = [
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
]

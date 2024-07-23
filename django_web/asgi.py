import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from Notifications.urls import urlpatterns  # Replace with your actual app name

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_web.settings')  # Replace with your actual project name

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            urlpatterns
        )
    ),
})

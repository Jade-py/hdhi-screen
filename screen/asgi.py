import os
from channels.routing import ProtocolTypeRouter, URLRouter
from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
import base.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'screen.settings')

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": ASGIStaticFilesHandler(django_asgi_app),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            base.routing.websocket_urlpatterns
        )
    ),
})

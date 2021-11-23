from django.conf.urls import url

from .consumers import ChatConsumer

websocket_urlpatterns = [
    url('', ChatConsumer.as_asgi())
]

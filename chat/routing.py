from django.urls import re_path

from . import consumers
# created with help of Django channels documentation: https://channels.readthedocs.io/en/latest/
websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]
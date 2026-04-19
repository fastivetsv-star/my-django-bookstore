from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Адреса, по якій браузер буде підключатися до сокета
    re_path(r'ws/notifications/$', consumers.OrderNotificationConsumer.as_asgi()),
]
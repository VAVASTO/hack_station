from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/some_path/$', consumers.SomeConsumer.as_asgi()),
    re_path(r'ws/get_map/$', consumers.GetMap.as_asgi()),
    re_path(r'ws/set_position/$', consumers.SetPosition.as_asgi()),
    re_path(r'ws/start_autopilot/$', consumers.TurnAutopilotOn.as_asgi()),
    re_path(r'ws/get_position/$', consumers.GetPosition.as_asgi()),
    # Добавьте другие URL-паттерны, если необходимо
]
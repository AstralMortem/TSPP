from django.urls import path

from . import views
from .consumers import ChatConsumer

app_name = "chat"
urlpatterns = [
    path("", views.chat_view, name="view"),
    path("list/", views.ChatList.as_view(), name="list"),
    path("contacts/", views.ChatList.as_view(), name="contacts"),
    path("create/<int:user_id>/", views.create_room, name="create"),
    path("join/<uuid:chat_id>/", views.join_room, name="join"),
]

websocket_urlpatterns = [
    path("chat/<uuid:chat_id>", ChatConsumer.as_asgi()),
]

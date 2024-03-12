import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from account.models import Squad, Volunter

from chat.models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        my_id = self.user.pk
        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.chat_name = "chat_%s" % self.chat_id

        await self.channel_layer.group_add(self.chat_name, self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        print(data)
        message = data["message"]
        username = await self.get_username(self.user.pk)
        recipient = await self.get_another_user(self.chat_id)

        message_date = await self.save_message(recipient, message, username)

        await self.channel_layer.group_send(
            self.chat_name,
            {
                "type": "chat_message",
                "message": message,
                "username": username,
                "recipient": recipient.pk,
                "sender": self.user.pk,
                "date": str(message_date.hour) + ":" + str(message_date.minute),
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        sender_id = event["sender"]
        date = event["date"]
        message_html = f"<div hx-swap-oob='beforeend:#messages'><div id='message-{sender_id}' class='notification p-2'><div class='is-flex is-flex-direction-row is-justify-content-space-between gap-10'><p class='title is-5 mb-0'><b>{username}</b></p><p class='is-size-7'>{date}</p></div>{str(message)}</div></div>"

        await self.send(text_data=str({"message": message_html, "username": username}))

    async def disconnect(self, code):
        self.channel_layer.group_discard(self.chat_name, self.channel_name)

    @sync_to_async
    def save_message(self, recipient, message, username):
        sender = self.user
        chat = Chat.objects.get(pk=self.chat_id)
        msg = Message.objects.create(
            chat=chat,
            sender=sender,
            recipient=recipient,
            message=message,
            username=username,
        )
        return msg.created

    @sync_to_async
    def get_username(self, user_id):
        role = self.user.get_role()
        if role == "Volunter":
            return str(Volunter.objects.get(pk=user_id))
        elif role == "Squad":
            return str(Squad.objects.get(pk=user_id))
        else:
            return self.user.email

    @sync_to_async
    def get_another_user(self, chat_id):
        chat = Chat.objects.get(pk=chat_id)
        if chat.user1 == self.user:
            return chat.user2
        else:
            return chat.user1

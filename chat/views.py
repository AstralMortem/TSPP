from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Chat, Message
from django.contrib.auth import get_user_model


def chat_view(request):
    return render(request, "chat/chat_view.html")


def contacts(request):
    users = get_user_model().objects.exclude(pk=request.user.pk)
    return render(request, "chat/contacts.html", {"users": users})


class ChatList(generic.ListView):
    model = Chat
    template_name = "chat/list.html"


def create_room(request, user_id):
    if request.method == "POST":
        user_1 = get_user_model().objects.get(pk=request.user.pk)
        user_2 = get_user_model().objects.get(pk=user_id)
        chat = Chat.dialog_exists(user_1, user_2)
        if not chat:
            chat = Chat.objects.create(user1=user_1, user2=user_2)
            chat.save()
        return HttpResponseRedirect(
            reverse_lazy("chat:join", kwargs={"chat_id": chat.pk})
        )
    else:
        return HttpResponseBadRequest("Not alowed")


def join_room(request, chat_id):
    chat = Chat.objects.get(pk=chat_id)
    messages = Message.objects.filter(chat=chat)
    context = {
        "chat_room": chat,
        "messages": messages,
    }
    return render(request, "chat/room.html", context)

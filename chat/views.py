from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from .models import Chat, Message
from django.contrib.auth import get_user_model


def chat_view(request):
    return render(request, "chat/chat_view.html")


class ContactsList(generic.ListView):
    model = get_user_model()
    paginate_by = 2
    template_name = "chat/contacts.html"
    context_object_name = "users"

    def get_queryset(self):
        qs = super().get_queryset()
        qs.exclude(pk=self.request.user.pk)
        filter_search = self.request.GET.get("search")
        if filter_search:
            qs = qs.filter(
                Q(role__title__icontains=filter_search)
                | Q(email__icontains=filter_search)
            )
        return qs


class ChatList(generic.ListView):
    model = Chat
    template_name = "chat/list.html"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(Q(user1=self.request.user) | Q(user2=self.request.user))
        filter_search = self.request.GET.get("search")
        if filter_search:
            qs = qs.filter(
                Q(user1__role__title__icontains=filter_search)
                | Q(user2__role__title__icontains=filter_search)
                | Q(user1__email__icontains=filter_search)
                | Q(user2__email__icontains=filter_search)
            )
        print(qs)
        return qs


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
        "chat": chat,
        "messages": messages,
    }
    return render(request, "chat/room.html", context)

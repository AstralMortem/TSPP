from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from orders.views import index


from django.views.generic import ListView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from typing import List


UserModel = get_user_model()


class UsersListView(LoginRequiredMixin, ListView):
    http_method_names = [
        "get",
    ]

    def get_queryset(self):
        return UserModel.objects.all().exclude(id=self.request.user.id)

    def render_to_response(self, context, **response_kwargs):
        users: List[AbstractBaseUser] = context["object_list"]

        data = [{"username": user.get_username(), "pk": str(user.pk)} for user in users]
        return JsonResponse(data, safe=False, **response_kwargs)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls"), name="account"),
    path("cabinet/", include("orders.urls"), name="orders"),
    path("cabinet/", include("fundraising.urls"), name="fundraising"),
    path("", index, name="home"),
    path("chat/", include("chat_depricated.urls"), name="chat"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

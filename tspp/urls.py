from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from orders.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls"), name="account"),
    path("cabinet/", include("orders.urls"), name="orders"),
    path("cabinet/", include("fundraising.urls"), name="fundraising"),
    path("", index, name="home"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

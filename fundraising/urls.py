from django.urls import path
from .views import (
    FundraisingCreateView,
    FundraisingDeleteView,
    FundraisingDetailView,
    FundraisingListView,
    FundraisingUpdateView,
    FundraisingCategoryListView,
    fundraising_view,
)

app_name = "fundraising"
urlpatterns = [
    path("fundraising/view", fundraising_view, name="view"),
    path("fundraising/", FundraisingListView.as_view(), name="list"),
    path(
        "fundraising/category/", FundraisingCategoryListView.as_view(), name="category"
    ),
    path("fundraising/add", FundraisingCreateView.as_view(), name="add"),
    path("fundraising/<int:pk>/", FundraisingDetailView.as_view(), name="detail"),
    path(
        "fundraising/<int:pk>/change/", FundraisingUpdateView.as_view(), name="update"
    ),
    path("fundraising/<int:pk>/delete", FundraisingDeleteView.as_view(), name="delete"),
]

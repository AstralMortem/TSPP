from django.urls import path
from .views import (
    FundraisingCreateView,
    FundraisingDeleteView,
    FundraisingDetailView,
    FundraisingListView,
    FundraisingUpdateView,
    FundraisingCategoryListView,
    Donate,
    MyFundraisingDetailView,
    MyFundraisingListView,
    fundraising_view,
    my_fundraising_view,
    complete,
)

app_name = "fundraising"
urlpatterns = [
    path("fundraising/view", fundraising_view, name="view"),
    path("fundraising/view/my", my_fundraising_view, name="my-view"),
    path("fundraising/", FundraisingListView.as_view(), name="list"),
    path("fundraising/my", MyFundraisingListView.as_view(), name="my-list"),
    path(
        "fundraising/category/", FundraisingCategoryListView.as_view(), name="category"
    ),
    path("fundraising/add", FundraisingCreateView.as_view(), name="add"),
    path("fundraising/<int:pk>/", FundraisingDetailView.as_view(), name="detail"),
    path(
        "fundraising/<int:pk>/my", MyFundraisingDetailView.as_view(), name="my-detail"
    ),
    path(
        "fundraising/<int:pk>/change/", FundraisingUpdateView.as_view(), name="update"
    ),
    path("fundraising/<int:pk>/delete", FundraisingDeleteView.as_view(), name="delete"),
    path("donate/<int:fundraising_id>/", Donate.as_view(), name="donate"),
    path("fundraising/<int:pk>/complete/", complete, name="complete"),
]

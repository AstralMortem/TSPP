from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    UserLoginView,
    user_signup,
    user_signup_next,
    user_signup_complete,
    user_profile,
    squad_view,
    SquadDetailView,
    SquadListView,
    SquadCategory,
)

app_name = "account"

urlpatterns = [
    # auth
    path("login/", UserLoginView.as_view(next_page="/"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/account/login"), name="logout"),
    path("signup/next/<int:pk>/", user_signup_next, name="signup-next"),
    path("signup/complete", user_signup_complete, name="signup-complete"),
    path("signup/", user_signup, name="signup"),
    # profile
    path("profile/", user_profile, name="profile"),
    # squad
    path("squad/view/", squad_view, name="squad-view"),
    path("squad/category/", SquadCategory.as_view(), name="squad-category"),
    path("squad/<int:pk>/", SquadDetailView.as_view(), name="squad-detail"),
    path("squad/", SquadListView.as_view(), name="squad-list"),
]

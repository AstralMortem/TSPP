from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    UserLoginView,
    user_signup,
    user_signup_next,
    user_signup_complete,
    user_profile,
    user_fundraising,
    user_orders,
)

app_name = "account"

urlpatterns = [
    path("login/", UserLoginView.as_view(next_page="/"), name="login"),
    path("logout/", LogoutView.as_view(next_page="/account/login"), name="logout"),
    path(
        "signup/next/<int:pk>/",
        user_signup_next,
        name="signup-next",
    ),
    path("signup/complete", user_signup_complete, name="signup-complete"),
    path("signup/", user_signup, name="signup"),
    path("profile/", user_profile, name="profile"),
    path("profile/orders", user_orders, name="my-orders"),
    path("profile/fundraising", user_fundraising, name="my-fundraising"),
]

from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView
from .forms import SquadCreate, VolunterCreate, UserCreate


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = "account/login.html"


def user_signup(request):
    if request.method == "POST":
        form = UserCreate(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(
                reverse_lazy("account:signup-next", kwargs={"pk": user.pk})
            )
    else:
        form = UserCreate()
    return render(request, "account/signup.html", {"form": form, "step": 1})


def user_signup_next(request, pk):
    base_user = get_user_model().objects.get(pk=pk)
    form = None
    if request.method == "POST":
        if base_user.role.title == "Volunter":
            form = VolunterCreate(request.POST)
        elif base_user.role.title == "Squad":
            form = SquadCreate(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user = base_user
            user.save()
            return HttpResponseRedirect(reverse_lazy("account:signup-complete"))
    else:
        if base_user.role.title == "Volunter":
            form = VolunterCreate()
        elif base_user.role.title == "Squad":
            form = SquadCreate()
    return render(request, "account/signup.html", {"form": form, "step": 2})


def user_signup_complete(request):
    return render(request, "account/complete.html", {"step": 3})

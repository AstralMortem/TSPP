from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView

from orders.models import Order
from .forms import SquadCreate, VolunterCreate, UserCreate
from .models import Admin, Squad, SquadType, Volunter


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = "account/login.html"


def user_profile(request):
    user_role = request.user.role.title
    if user_role == "Volunter":
        profile = Volunter.objects.get(user=request.user)
    elif user_role == "Squad":
        profile = Squad.objects.get(user=request.user)
    else:
        profile = Admin.objects.get(user=request.user)
    return render(request, "account/profile.html", {"profile": profile})


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


class SquadCategory(generic.ListView):
    model = SquadType
    template_name = "components/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["path"] = reverse("account:squad-list")
        return context


class SquadListView(generic.ListView):
    paginate_by = 4
    model = Squad
    template_name = "account/squad_list.html"

    def get_queryset(self):
        qs = self.model.objects.all()
        filter_search = self.request.GET.get("search")
        filter_category = self.request.GET.get("category")

        if filter_search:
            qs = self.model.objects.filter(squad_name__icontains=filter_search)
        if filter_category:
            qs = self.model.objects.filter(squad_type__pk=filter_category)

        if not filter_category and not filter_search:
            return super().get_queryset()
        return qs


class SquadDetailView(generic.DetailView):
    template_name = "account/profile.html"
    context_object_name = "profile"
    model = Squad


def squad_view(request):
    return render(request, "account/squad_view.html")


def volunter_view(request):
    return render(request, "account/volunter_view.html")

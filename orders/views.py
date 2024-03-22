from turtle import title
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from account.models import Squad, Volunter
from .models import Category, Order
from django import forms


def index(request):
    context = {}
    if request.user.is_authenticated:
        context = {"redirect_path": reverse("fundraising:view")}

    return render(request, "index.html", context)


# ============ Orders section =========================


def order_view(request):
    return render(request, "orders/orders_view.html")


def take_order(request, pk):
    order = Order.objects.get(pk=pk)
    volunter_profile = Volunter.objects.get(pk=request.user.pk)
    order.volunter = volunter_profile
    order.is_taken = True
    order.taked_at = timezone.now()
    order.save()
    return HttpResponse("Упішно взято")


def untake_order(request, pk):
    order = Order.objects.get(pk=pk)
    order.volunter = None
    order.is_taken = False
    order.taked_at = None
    order.save()
    return HttpResponse("Упішно вилучено")


def remove_contractor(request, pk):
    order = Order.objects.get(pk=pk)
    order.volunter = None
    order.is_taken = False
    order.taked_at = None
    order.save()
    return HttpResponse("Упішно вилучено")


def mark_completed(request, pk):
    order = Order.objects.get(pk=pk)
    order.completed_at = timezone.now()
    order.is_completed = True
    order.save()
    return HttpResponse("Упішно виконано")


class OrdersCategoryListView(generic.ListView):
    model = Category
    template_name = "components/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["path"] = reverse("orders:list")
        return context


class OrdersListView(generic.ListView):
    paginate_by = settings.DEFAULT_PAGINATION
    model = Order
    template_name = "orders/list.html"

    def get_queryset(self):
        qs = Order.objects.filter(is_taken=False)
        filter_search = self.request.GET.get("search")
        filter_category = self.request.GET.get("category")
        filter_user = self.request.GET.get("initiator")
        if filter_search:
            qs = qs.filter(title__icontains=filter_search)
        if filter_category:
            qs = qs.filter(category__pk=filter_category)
        if filter_user:
            qs = qs.filter(squad__pk=filter_user)
        return qs


class OrdersDetailView(generic.DetailView):
    model = Order
    template_name = "orders/orders_detail.html"


class OrdersDeleteView(generic.DeleteView):
    model = Order
    template_name = "components/delete_form.html"
    success_url = reverse_lazy("orders:view")


class OrdersCreateView(generic.CreateView):
    model = Order
    template_name = "components/create_form.html"
    fields = ["title", "info", "category"]
    success_url = "/"

    def form_valid(self, form: forms.BaseModelForm) -> HttpResponse:
        order = form.instance
        order.squad = Squad.objects.get(user=self.request.user)
        return super(OrdersCreateView, self).form_valid(form)


class OrdersUpdateView(generic.UpdateView):
    model = Order
    template_name = "components/update_form.html"
    fields = ["title", "info", "category"]

    def get_success_url(self) -> str:
        obj = self.get_object()
        return reverse_lazy("orders:detail", kwargs={"pk": obj.pk})


class MyOrdersListView(OrdersListView):
    template_name = "my_orders/my_orders_list.html"

    def get_queryset(self):
        filter_search = self.request.GET.get("search")
        user = self.request.user
        qs = self.model.objects.all()
        role = user.get_role()
        if role == "Volunter":
            qs = qs.filter(volunter__pk=user.pk)
        elif role == "Squad":
            qs = qs.filter(squad__pk=user.pk)
        if filter_search:
            qs = qs.filter(title__icontains=filter_search)
        return qs


class MyOrdersDetailView(OrdersDetailView):
    template_name = "my_orders/my_orders_detail.html"


def my_orders_view(request):
    return render(request, "my_orders/my_orders_view.html")

from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import generic

from account.models import Squad
from .models import Category, Order
from django import forms


def index(request):
    return render(request, "index.html")


# ============ Orders section =========================


def order_view(request):
    return render(request, "orders/orders_view.html")


def take_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.volunter = request.user
    order.is_taken = True
    order.taked_at = timezone.now()
    order.save()
    return HttpResponse("Упішно взято")


class OrdersCategoryListView(generic.ListView):
    model = Category
    template_name = "components/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["path"] = reverse("orders:list")
        return context


class OrdersListView(generic.ListView):
    paginate_by = 4
    model = Order
    template_name = "orders/list.html"

    def get_queryset(self):
        qs = Order.objects.all()
        filter_search = self.request.GET.get("search")
        filter_category = self.request.GET.get("category")
        if filter_search:
            qs = Order.objects.filter(title__icontains=filter_search)
        if filter_category:
            qs = Order.objects.filter(category__pk=filter_category)
        if not filter_category and not filter_search:
            return super().get_queryset()
        return qs


class OrdersDetailView(generic.DetailView):
    model = Order
    template_name = "orders/orders_detail.html"


class OrdersDeleteView(generic.DeleteView):
    model = Order
    template_name = "components/delete_form.html"
    success_url = reverse_lazy("orders:orders-view")


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

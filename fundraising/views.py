from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic
from .models import Fundraising, Transaction
from account.models import Squad
from orders.models import Category


def fundraising_view(request):
    return render(request, "fundraising/fundraising_view.html")


class Donate(generic.CreateView):
    model = Transaction
    fields = ["amount"]
    template_name = "fundraising/donate_form.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form = form.save(commit=False)
        form.fundraising = Fundraising.objects.get(pk=self.kwargs.get("fundraising_id"))
        form.user = self.request.user
        print(self.kwargs)
        form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:

        return reverse(
            "fundraising:detail", kwargs={"pk": self.kwargs.get("fundraising_id")}
        )


class FundraisingCategoryListView(generic.ListView):
    model = Category
    template_name = "components/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["path"] = reverse("fundraising:list")
        return context


class FundraisingListView(generic.ListView):
    paginate_by = 4
    model = Fundraising
    template_name = "fundraising/list.html"

    def get_queryset(self):
        qs = Fundraising.objects.all()
        filter_search = self.request.GET.get("search")
        filter_category = self.request.GET.get("category")
        filter_user = self.request.GET.get("initiator")
        if filter_search:
            qs = Fundraising.objects.filter(title__icontains=filter_search)
        if filter_category:
            qs = Fundraising.objects.filter(category__pk=filter_category)
        if filter_user:
            qs = Fundraising.objects.filter(squad__pk=filter_user)
        if not filter_category and not filter_search and not filter_user:
            return super().get_queryset()
        return qs


class FundraisingDetailView(generic.DetailView):
    model = Fundraising
    template_name = "fundraising/fundraising_detail.html"


class FundraisingDeleteView(generic.DeleteView):
    model = Fundraising
    template_name = "components/delete_form.html"
    success_url = reverse_lazy("fundraising:view")


class FundraisingCreateView(generic.CreateView):
    model = Fundraising
    template_name = "components/create_form.html"
    fields = ["title", "info", "category", "price"]
    success_url = "/"

    def form_valid(self, form):
        fund = form.instance
        fund.squad = Squad.objects.get(user=self.request.user)
        return super(FundraisingCreateView, self).form_valid(form)


class FundraisingUpdateView(generic.UpdateView):
    model = Fundraising
    template_name = "components/update_form.html"
    fields = ["title", "info", "category", "price"]

    def get_success_url(self) -> str:
        obj = self.get_object()
        return reverse_lazy("fundraising:detail", kwargs={"pk": obj.pk})

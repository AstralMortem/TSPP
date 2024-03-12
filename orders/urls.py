from django.urls import path, re_path
from .views import (
    MyOrdersDetailView,
    MyOrdersListView,
    my_orders_view,
    order_view,
    OrdersListView,
    OrdersDetailView,
    OrdersDeleteView,
    OrdersCreateView,
    OrdersUpdateView,
    OrdersCategoryListView,
    take_order,
    untake_order,
    remove_contractor,
    mark_completed,
)

app_name = "orders"
urlpatterns = [
    path("orders/view", order_view, name="view"),
    path("orders/view/my", my_orders_view, name="my-view"),
    path("orders/", OrdersListView.as_view(), name="list"),
    path("orders/my/", MyOrdersListView.as_view(), name="my-list"),
    path("orders/category", OrdersCategoryListView.as_view(), name="category"),
    path("orders/add", OrdersCreateView.as_view(), name="add"),
    path("orders/<int:pk>/", OrdersDetailView.as_view(), name="detail"),
    path("orders/<int:pk>/my/", MyOrdersDetailView.as_view(), name="my-detail"),
    path("orders/<int:pk>/change/", OrdersUpdateView.as_view(), name="update"),
    path("orders/<int:pk>/delete/", OrdersDeleteView.as_view(), name="delete"),
    path("orders/<int:pk>/take/", take_order, name="take"),
    path("orders/<int:pk>/untake/", untake_order, name="untake"),
    path(
        "orders/<int:pk>/untake_contractor/",
        remove_contractor,
        name="untake-contractor",
    ),
    path("orders/<int:pk>/complete/", mark_completed, name="complete"),
]

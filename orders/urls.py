from django.urls import path, re_path
from .views import (
    order_view,
    OrdersListView,
    OrdersDetailView,
    OrdersDeleteView,
    OrdersCreateView,
    OrdersUpdateView,
    OrdersCategoryListView,
    take_order,
)

app_name = "orders"
urlpatterns = [
    path("orders/view", order_view, name="view"),
    path("orders/", OrdersListView.as_view(), name="list"),
    path("orders/category", OrdersCategoryListView.as_view(), name="category"),
    path("orders/add", OrdersCreateView.as_view(), name="add"),
    path("orders/<int:pk>/", OrdersDetailView.as_view(), name="detail"),
    path("orders/<int:pk>/change/", OrdersUpdateView.as_view(), name="update"),
    path("orders/<int:pk>/delete", OrdersDeleteView.as_view(), name="delete"),
    path("orders/<int:pk>/take/", take_order, name="take"),
]

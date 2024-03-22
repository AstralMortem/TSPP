from django.test import TestCase
from django.urls import resolve, reverse
from orders import views
from django.conf import settings

# Create your tests here.
class OrdersPageTest(TestCase):
    def test_orders_page_status_code(self):
        response = self.client.get(reverse('orders:view'))
        self.assertEqual(response.status_code, 200)

    def test_if_pagination_settings_exist(self):
        try:
            obj = getattr(settings,"DEFAULT_PAGINATION")
        except AttributeError:
            self.fail("Not exist")

    def test_pagination_orders(self):
        order_view = views.OrdersListView
        my_order_view = views.MyOrdersListView
        self.assertEquals(order_view.paginate_by, settings.DEFAULT_PAGINATION)
        self.assertEquals(my_order_view.paginate_by, settings.DEFAULT_PAGINATION)
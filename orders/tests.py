from unicodedata import category
from django.test import TestCase
from django.urls import resolve, reverse
from account.models import Squad, User, SquadType, Volunter, VolunterType
from orders import views
from django.conf import settings

from orders.models import Category, Order


# Create your tests here.
class OrdersPageTest(TestCase):
    def test_orders_page_status_code(self):
        response = self.client.get(reverse("orders:view"))
        self.assertEqual(response.status_code, 200)

    def test_if_pagination_settings_exist(self):
        try:
            obj = getattr(settings, "DEFAULT_PAGINATION")
        except AttributeError:
            self.fail("Not exist")

    def test_pagination_orders(self):
        order_view = views.OrdersListView
        my_order_view = views.MyOrdersListView
        self.assertEquals(order_view.paginate_by, settings.DEFAULT_PAGINATION)
        self.assertEquals(my_order_view.paginate_by, settings.DEFAULT_PAGINATION)


class TestOrderCreation(TestCase):
    def test_normal_order_creation(self):
        user = User.objects.create()
        self.assertNotEqual(user, None)
        squad_type = SquadType.objects.create(name="test_type")
        self.assertNotEqual(squad_type, None)
        squad = Squad.objects.create(user=user, squad_type=squad_type)
        self.assertNotEqual(squad, None)
        order = Order.objects.create(
            squad=squad,
            title="test",
            info="test",
            category=Category.objects.all().first(),
        )
        self.assertNotEqual(order, None)

    def test_unrole_user_order_creation(self):
        user = User.objects.create()
        self.assertNotEqual(user, None)
        self.assertRaises(
            ValueError,
            Order,
            squad=user,
            title="test",
            info="test",
            category=Category.objects.all().first(),
        )

    def test_volunter_order_creation(self):
        user = User.objects.create()
        self.assertNotEqual(user, None)
        volunter_type = VolunterType.objects.create(name="test_type")
        self.assertNotEqual(volunter_type, None)
        volunter = Volunter.objects.create(user=user, volunter_type=volunter_type)
        self.assertNotEqual(volunter, None)
        self.assertRaises(
            TypeError,
            Order,
            squad=volunter,
            title="test",
            info="test",
            category=Category.objects.all().first(),
        )

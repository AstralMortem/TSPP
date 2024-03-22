from django.test import TestCase
from django.urls import resolve, reverse

from account.models import Squad
from . import views
from .models import Fundraising
from django.conf import settings

# Create your tests here.
class FundraisingPageTest(TestCase):
    def test_fundraising_page_status_code(self):
        response = self.client.get(reverse('fundraising:view'))
        self.assertEqual(response.status_code, 200)

    def test_if_pagination_settings_exist(self):
        try:
            obj = getattr(settings,"DEFAULT_PAGINATION")
        except AttributeError:
            self.fail("Not exist")

    def test_pagination_fundraising(self):
        order_view = views.FundraisingListView
        my_order_view = views.MyFundraisingListView
        self.assertEquals(order_view.paginate_by, settings.DEFAULT_PAGINATION)
        self.assertEquals(my_order_view.paginate_by, settings.DEFAULT_PAGINATION)

    def make_order(self,sq):
        obj = Fundraising.objects.create(title='title',info='test',squad_id=sq,price=1000)
        return obj
    
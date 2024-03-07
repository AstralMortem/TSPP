from django.db import models
from django.utils.translation import gettext_lazy as _
from utils.models import IOrder


class Category(models.Model):
    name = models.CharField(_("Order category name"), max_length=249)

    def __str__(self):
        return self.name


class Order(IOrder):
    volunter = models.ForeignKey(
        "account.Volunter",
        verbose_name=_("Contractor"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    is_taken = models.BooleanField(_("Is taken"), default=False)
    taked_at = models.DateTimeField(null=True, blank=True)

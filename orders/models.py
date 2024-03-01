from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class OrderCategory(models.Model):
    name = models.CharField(_("Order category name"), max_length=249)

    def __str__(self):
        return self.name


# order interface
class IOrder(models.Model):
    title = models.CharField(_("Title"), max_length=249)
    info = models.TextField(_("Description"))
    squad = models.ForeignKey(
        "account.Squad", verbose_name=_("Initiator"), on_delete=models.PROTECT
    )
    category = models.ForeignKey(OrderCategory, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    # override save method
    # when models saved check if is_completed
    # then set completed_at date-time

    def save(self, *args, **kwargs):
        if self.is_completed:
            self.completed_at = timezone.now()
        super(IOrder, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class Order(IOrder):
    volunter = models.ForeignKey(
        "account.Volunter", verbose_name=_("Contractor"), on_delete=models.PROTECT
    )
    is_taken = models.BooleanField(_("Is taken"), default=False)
    taked_at = models.DateTimeField(null=True, blank=True)


class Fundraising(IOrder):
    price = models.DecimalField(max_digits=9, decimal_places=2)


class Transaction(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.SET_NULL, null=True)
    fundraising = models.ForeignKey("Fundraising", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.user.email

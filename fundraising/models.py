from django.db import models
from utils.models import IOrder


class Fundraising(IOrder):
    price = models.DecimalField(max_digits=9, decimal_places=2)


class Transaction(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.SET_NULL, null=True)
    fundraising = models.ForeignKey("Fundraising", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.user.email

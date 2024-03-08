from django.db import models
from utils.models import IOrder


class Transaction(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.SET_NULL, null=True)
    fundraising = models.ForeignKey("Fundraising", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.user)


class Fundraising(IOrder):
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def get_donated_amount(self):
        res = 0
        for transaction in Transaction.objects.filter(fundraising=self):
            res += transaction.amount
        return res

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class IOrder(models.Model):
    title = models.CharField(_("Title"), max_length=249)
    info = models.TextField(_("Description"))
    squad = models.ForeignKey(
        "account.Squad", verbose_name=_("Initiator"), on_delete=models.PROTECT
    )
    category = models.ForeignKey(
        "orders.Category", on_delete=models.SET_NULL, null=True
    )
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
        ordering = ["created_at"]

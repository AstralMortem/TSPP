from tabnanny import verbose
import uuid
from django.db import models
from django.db.models import Q
from model_utils.models import TimeStampedModel
from django.contrib.auth import get_user_model


# Create your models here.
class Chat(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    user1 = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="+"
    )
    user2 = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="+"
    )

    def __str__(self):
        return f"Chat between {self.user1} and {self.user2}"

    @staticmethod
    def dialog_exists(u1, u2):
        return Chat.objects.filter(
            Q(user1=u1, user2=u2) | Q(user1=u2, user2=u1)
        ).first()

    class Meta:
        unique_together = (("user1", "user2"), ("user2", "user1"))


class Message(TimeStampedModel):
    id = models.BigAutoField(primary_key=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    username = models.TextField(null=True, blank=True)
    sender = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="from_user",
        db_index=True,
    )
    recipient = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="to_user",
        db_index=True,
    )
    message = models.TextField(blank=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ("created",)

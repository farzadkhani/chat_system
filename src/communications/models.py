from django.db import models
from django.contrib.auth import get_user_model

from main_app.models import ModelMixin

# Create your models here.

User = get_user_model()


class Message(ModelMixin):
    """
    model for messages between users base on ModelMixin class for soft delete
    with quote_to field for quote to another message
    short_text property for short text of message in admin panel
    """

    class Meta:
        verbose_name = "Message model"
        verbose_name_plural = "Messages model"

    text = models.TextField()
    sender = models.ForeignKey(
        User,
        related_name="sent_messages",
        on_delete=models.CASCADE,
    )
    receiver = models.ForeignKey(
        User,
        related_name="received_messages",
        on_delete=models.CASCADE,
    )
    quote_to = models.ForeignKey(
        "self",
        related_name="quoted_messages",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"

    @property
    def short_text(self):
        return self.text[:20]

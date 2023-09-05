from django.db import models
from django.contrib.auth import get_user_model

from main_app.models import ModelMixin
from communications.models import Message

# Create your models here.

User = get_user_model()


class Notification(ModelMixin):
    """
    model for notifications base on ModelMixin class for soft delete
    """
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
    )
    code = models.CharField(max_length=256)
    message = models.ForeignKey(
        Message,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    is_read = models.BooleanField(default=False)
    description = models.TextField()

    class Meta:
        ordering = ("-id",)

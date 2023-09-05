from django.contrib import admin

from .models import Notification
from main_app.admin import ModelAdminMixin


# Register your models here.
@admin.register(Notification)
class NotificationModelAdmin(ModelAdminMixin):
    list_display = (
        "id",
        "user",
        "code",
        "message",
        "is_read",
        "description",
        "created_at",
    )
    raw_id_fields = ("message", "user")
    list_filter = ("created_at", "is_read", "code", "user")
    date_hierarchy = "created_at"

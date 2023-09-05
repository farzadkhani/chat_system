from django.contrib import admin

from main_app.admin import ModelAdminMixin

from .models import Message

# Register your models here.


@admin.register(Message)
class MessageModelAdmin(ModelAdminMixin):
    list_display = [
        "id",
        "sender",
        "receiver",
        "quote_to",
        "is_read",
        "is_soft_deleted",
        "created_at",
        "updated_at",
        "short_text",
    ]

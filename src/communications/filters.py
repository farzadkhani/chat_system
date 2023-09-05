from django_filters import rest_framework as filters

from .models import Message


class MessageFilterSet(filters.FilterSet):
    """
    Filters for Message model base on FilterSet class and
    sender, receiver, quote_to and is_read fields of model
    """

    class Meta:
        model = Message
        fields = {
            "sender": ["exact"],
            "receiver": ["exact"],
            "quote_to": ["exact"],
            "is_read": ["exact"],
        }

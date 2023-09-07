from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):
    """
    Serializer for get User model base on ModelSerilizer
    and basic fields of model
    """

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",
        ]

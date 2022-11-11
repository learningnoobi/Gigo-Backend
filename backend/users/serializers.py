from rest_framework import serializers
from .models import User


class UserLessSerializer(serializers.ModelSerializer):
    role = serializers.StringRelatedField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "avatar", "role", "bio", "iroha_name"]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 6},
        }

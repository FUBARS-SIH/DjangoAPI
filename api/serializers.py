from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import CustomUser, Authority

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'id', 
            'username',
            'email',
            'password',
            'is_authority',
        )
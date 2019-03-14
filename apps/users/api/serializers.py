from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()


class UserAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'gender', 'name', 'birth_date',)

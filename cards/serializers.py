from rest_framework import serializers

from cards.models import Card
from users.models import User


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']

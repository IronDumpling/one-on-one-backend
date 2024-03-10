from rest_framework import serializers
from django.contrib.auth.models import User
from ..models.contact import Contact

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ContactSerializer(serializers.ModelSerializer):
    user1_detail = UserSerializer(source='user1', read_only=True)
    user2_detail = UserSerializer(source='user2', read_only=True)

    class Meta:
        model = Contact
        fields = ['id', 'user1', 'user2', 'user1_detail', 'user2_detail']


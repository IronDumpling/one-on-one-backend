from rest_framework import serializers
from ..models.contact import Contact

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['id', 'user1', 'user2', 'alias1', 'alias2']

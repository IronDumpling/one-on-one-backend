from rest_framework import serializers
from ..models.contact import Contact

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ['id', 'user1', 'user2', 'alias1', 'alias2']


class ContactInfoSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    alias = serializers.SerializerMethodField()

    def __init__(self, contact, request_user):
        self.request_user = request_user
        super().__init__(contact)

    def get_user_id(self, obj):
        if self.request_user == obj.user1:
            return obj.user2.id
        else:
            return obj.user1.id

    def get_alias(self, obj):
        if self.request_user == obj.user1:
            return obj.alias2
        else:
            return obj.alias1

    class Meta:
        model = Contact
        fields = ['id', 'user_id', 'alias']

class ContactUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['alias1', 'alias2']
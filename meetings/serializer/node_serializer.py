from rest_framework import serializers
from ..models import node


class NodeSerializer(serializers.ModelSerializer):

    meeting = serializers.ReadOnlyField(source='meeting.name')

    class Meta:
        model = node.Node
        fields = '__all__'

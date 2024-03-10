from rest_framework import serializers
from ..models import event


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = event.Event
        fields = '__all__'

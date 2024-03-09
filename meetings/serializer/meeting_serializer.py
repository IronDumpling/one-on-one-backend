from rest_framework import serializers
from ..models import meeting


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = meeting.Meeting
        fields = ('name', 'description', 'state')
        
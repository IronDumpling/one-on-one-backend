from rest_framework import serializers
from ..models import member


class CalendarSerializer(serializers.ModelSerializer):

    class Meta:
        model = member.Member
        fields = '__all__'

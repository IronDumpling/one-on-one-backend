from rest_framework import serializers
from ..models import calendar


class CalendarSerializer(serializers.ModelSerializer):

    class Meta:
        model = calendar.Calendar
        fields = '__all__'

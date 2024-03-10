from rest_framework import serializers
from ..models import member


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = member.Member
        fields = ['id','meeting', 'role','user']

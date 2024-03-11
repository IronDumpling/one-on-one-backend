from rest_framework import serializers
from ..models.node import RemindNode, JoinNode, SubmitNode, PollNode, StateNode


class RemindNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RemindNode
        fields = '__all__'


class JoinNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = JoinNode
        fields = '__all__'


class SubmitNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmitNode
        fields = '__all__'


class PollNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollNode
        fields = '__all__'


class StateNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateNode
        fields = '__all__'

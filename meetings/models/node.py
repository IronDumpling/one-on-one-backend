from django.db import models
from .meeting import Meeting
from .member import Member


class Node(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(Member, on_delete=models.CASCADE)


class RemindNode(Node):
    receiver = models.ForeignKey(Member)
    message = models.CharField(max_length=120)


class JoinNode(Node):
    receiver = models.ForeignKey(Member)


class SubmitNode(Node):
    pass


class PollNode(Node):
    pass


class StateNode(Node):
    pass


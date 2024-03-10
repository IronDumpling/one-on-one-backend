from django.db import models
from .meeting import Meeting
from .member import Member
from .calendar import Calendar


class Node(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    sender = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "node " + str(self.id)


class RemindNode(Node):
    receiver = models.ForeignKey(Member, on_delete=models.CASCADE)
    message = models.CharField(max_length=120)


class JoinNode(Node):
    receiver = models.ForeignKey(Member, on_delete=models.CASCADE)


class SubmitNode(Node):
    pass


class PollNode(Node):
    class PollState(models.TextChoices):
        ONGOING = 'on-going', 'On-Going State'
        FINISHED = 'finished', 'Finished State'
        CANCELED = 'canceled', 'Canceled State'

    state = models.CharField(choices=PollState, max_length=50, default=PollState.ONGOING)


class StateNode(Node):
    pass


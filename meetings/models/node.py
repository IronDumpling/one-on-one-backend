from django.db import models
from .meeting import Meeting
from .calendar import Calendar
from django.contrib.auth.models import User


class Node(models.Model):

    id = models.AutoField(primary_key=True, unique=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = False
        ordering = ('created_time', )

    def __str__(self):
        return "node " + str(self.id)


class RemindNode(Node):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=120, null=True)


class JoinNode(Node):
    receiver = models.ForeignKey(User, on_delete=models.CASCADE)


class SubmitNode(Node):
    pass


class PollNode(Node):
    class PollState(models.TextChoices):
        ONGOING = 'on-going', 'On-Going State'
        FINISHED = 'finished', 'Finished State'
        CANCELED = 'canceled', 'Canceled State'

    state = models.CharField(choices=PollState, max_length=50, default=PollState.ONGOING)
    users_voted = models.ManyToManyField(User, related_name='voted_polls', blank=True)

    def vote(self, user, selected_option):
        self.users_voted.add(user)
        Vote.objects.create(user=user, selected_option=selected_option)


class Option(models.Model):
    text = models.CharField(max_length=50)
    poll = models.ForeignKey(PollNode, on_delete=models.CASCADE, related_name='options')


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(PollNode, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(Option, on_delete=models.CASCADE)


class StateNode(Node):
    pass

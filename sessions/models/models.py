# temp file

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Calendar(models.Model):
    pass


class Event(models.Model):
    calendar = models.ForeignKey(Calendar)


class Session(models.Model):
    id = models.AutoField()
    calendar = models.ForeignKey(Calendar)
    users = models.CharField("1, 2, 3")


class MyUser(User):
    calendar = Session.objects.filter(id=event.calendar.id)
    pass


class Node(models.Model):
    session = models.ForeignKey(Session)
    time = models.DateTimeField(auto_now=True)
    sender = models.ForeignKey(MyUser)


class RemindNode(Node):
    receiver = models.ForeignKey(MyUser)
    message = models.CharField(max_length=120)


class JoinNode(Node):
    receiver = models.ForeignKey(MyUser)


class SubmitNode(Node):
    calendar = models.ForeignKey(Calendar)


class PollNode(Node):
    calendar = models.ForeignKey(Calendar)


class Member(models.Model):
    session = models.ForeignKey(Session)
    user = models.ForeignKey(MyUser)


class Contact(models.Model):
    user_1 = models.ForeignKey(MyUser)
    user_2 = models.ForeignKey(MyUser)





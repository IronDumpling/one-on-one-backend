# from django.db import models
# from django.utils import timezone
# from django.contrib.auth.models import User


# class Node(models.Model):
#     session = models.ForeignKey(Session)
#     time = models.DateTimeField(auto_now=True)
#     sender = models.ForeignKey(User)
#
#
# class RemindNode(Node):
#     receiver = models.ForeignKey(User)
#     message = models.CharField(max_length=120)
#
#
# class JoinNode(Node):
#     receiver = models.ForeignKey(User)
#
#
# class SubmitNode(Node):
#     calendar = models.ForeignKey(Calendar)
#
#
# class PollNode(Node):
#     calendar = models.ForeignKey(Calendar)
#
#
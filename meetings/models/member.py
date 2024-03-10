from django.db import models
from .meeting import Meeting
from django.contrib.auth.models import User


class Member(models.Model):

    ROLE_CHOICES = [
        ('host', 'Host'),
        ('member', 'Member'),
    ]


    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


    class Meta:
        unique_together = ['meeting', 'user']

    def __str__(self):
        return self.user.__str__()

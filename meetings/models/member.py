from django.db import models
from .meeting import Meeting
from django.contrib.auth.models import User


class Member(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.user.__str__()

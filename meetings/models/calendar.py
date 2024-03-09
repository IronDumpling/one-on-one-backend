from django.db import models
from .meeting import Meeting
from .member import Member


class Calendar(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    owner = models.ForeignKey(Member, on_delete=models.CASCADE)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.owner.__str__() + "'s calendar"

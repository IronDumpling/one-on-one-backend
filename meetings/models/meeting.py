from django.db import models


class Meeting(models.Model):
    class MeetingState(models.TextChoices):
        EDIT = 'edit', 'Edit State'
        READY = 'ready', 'Ready State'
        APPROVING = 'approving', 'Approving State'
        FINALIZED = 'finalized', 'Finalized State'

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=120, null=True)
    state = models.CharField(choices=MeetingState.choices, max_length=20, default=MeetingState.EDIT)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

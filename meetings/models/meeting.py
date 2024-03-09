from django.db import models
# from .calendar import Calendar


class Meeting(models.Model):
    class MeetingState(models.TextChoices):
        EDIT = 'edit', 'Edit State'
        READY = 'ready', 'Ready State'
        APPROVING = 'approving', 'Approving State'
        FINALIZED = 'finalized', 'Finalized State'

    id = models.AutoField(primary_key=True, unique=True)
    # calendar = models.ForeignKey(Calendar, on_delete=models.CASCADE)
    state = models.CharField(choices=MeetingState.choices, max_length=20, default=MeetingState.EDIT)


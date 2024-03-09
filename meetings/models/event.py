from django.db import models
from . import calendar


class Event(models.Model):
    class Availability(models.TextChoices):
        BUSY = 'busy', 'Busy State'
        MODERATE = 'moderate', 'Moderate State'
        AVAILABLE = 'available', 'Available State'

    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=120)
    availability = models.CharField(choices=Availability, max_length=20)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    calendar = models.ForeignKey(calendar.Calendar, on_delete=models.CASCADE)
    # Extra: repeat & end time


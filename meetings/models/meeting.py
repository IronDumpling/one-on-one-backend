from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Meeting(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    # calendar = models.ForeignKey(Calendar)
    # users = models.CharField("1, 2, 3")

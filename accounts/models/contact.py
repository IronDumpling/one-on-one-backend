from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')

from django.db import models
from django.contrib.auth.models import User


class Contact(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')
    alias1 = models.CharField(max_length=20, blank=True)
    alias2 = models.CharField(max_length=20, blank=True)


def get_contact(user1, user2):
    return Contact.objects.filter(
        models.Q(user1=user1, user2=user2) | models.Q(user1=user2, user2=user1)).first()
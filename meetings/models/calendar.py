from django.db import models
from .meeting import Meeting
from .member import Member
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Calendar(models.Model):

    id = models.AutoField(primary_key=True, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, editable=False)
    created_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)
        unique_together = ['meeting', 'owner']

    def __str__(self):
        return self.owner.__str__() + "'s calendar"
    
    def clean(self):

        # Check if the owner is associated with a member of the meeting
        if not self.meeting.member_set.filter(user=self.owner).exists():
            raise ValidationError("The owner must be a member of the meeting.")
        
        # Check if the meeting belongs to the owner
        if self.meeting.owner != self.owner:
            raise ValidationError("The meeting does not belong to the owner.")

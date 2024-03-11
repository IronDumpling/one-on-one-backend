from rest_framework import permissions
from .models.member import Member
from .models.calendar import Calendar
from .models.event import Event
from .models.meeting import Meeting

class IsMember(permissions.BasePermission):
    def has_permission(self, request, view, **kwargs):
        if request.user.is_authenticated:
            meeting_id = kwargs.get('meeting_id')
            return Member.objects.filter(user=request.user, meeting_id=meeting_id).exists()
        return False


# class IsMember(permissions.BasePermission):
#     """
#     Custom permission to only allow members of a meeting, calendar, or event to access it.
#     """
#     def has_object_permission(self, request, view, obj):
#         # Check for membership in Meeting directly
#         if isinstance(obj, Meeting):
#             return Member.objects.filter(meeting=meeting, user=request.user).exists()
        
#         # Check for membership through Calendar or Event's Meeting
#         elif isinstance(obj, Calendar) or isinstance(obj, Event):
#             meeting = obj.meeting
#             return Member.objects.filter(meeting=meeting, user=request.user).exists()
        
#         # Default deny if the object doesn't match
#         return False
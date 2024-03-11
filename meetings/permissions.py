from rest_framework import permissions
from .models.member import Member
from .models.calendar import Calendar
from .models.event import Event
from .models.meeting import Meeting

# class IsMember(permissions.BasePermission):
#     def has_permission(self, request, view, **kwargs):
#         if request.user.is_authenticated:
#             meeting_id = kwargs.get('meeting_id')
#             return Member.objects.filter(meeting_id=meeting_id).exists()
#         return False

class IsMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
        if isinstance(obj, Meeting):
            print('1')
            return obj.member_set.filter(user=request.user).exists()
        
        elif isinstance(obj, Calendar):
            print('2')
            return obj.meeting.member_set.filter(user=request.user).exists()
        
        elif isinstance(obj, Event):
            print('3')
            return obj.calendar.meeting.member_set.filter(user=request.user).exists()
        
        return False
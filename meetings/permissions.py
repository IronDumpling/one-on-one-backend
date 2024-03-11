from rest_framework import permissions
from .models.member import Member
from .models.calendar import Calendar
from .models.event import Event
from .models.meeting import Meeting


# class IsMember(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return Member.objects.filter(meeting_id=obj.id, user_id=request.user.id).exists()


# class IsMember(permissions.BasePermission):
#     def has_permission(self, request, view, **kwargs):
#         if request.user.is_authenticated:
#             meeting_id = kwargs.get('meeting_id')
#             return Member.objects.filter(meeting_id=meeting_id).exists()
#         return False

class IsMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("Is Member?")
        if not request.user.is_authenticated:
            print("Not authorized")
            return False

        if isinstance(obj, Meeting):
            print("Meeting")
            return obj.member_set.filter(user=request.user).exists()

        elif isinstance(obj, Calendar):
            print("Calendar")
            return obj.meeting.member_set.filter(user=request.user).exists()

        elif isinstance(obj, Event):
            print("Event")
            return obj.calendar.meeting.member_set.filter(user=request.user).exists()

        return False

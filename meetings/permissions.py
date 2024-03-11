from rest_framework import permissions
from .models.member import Member
from .models.calendar import Calendar
from .models.event import Event
from .models.node import Meeting


class IsMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Meeting):
            return obj.member_set.filter(user=request.user).exists()

        elif isinstance(obj, Member):
            return obj.meeting.member_set.filter(user=request.user).exists()

        elif isinstance(obj, Calendar):
            return obj.meeting.member_set.filter(user=request.user).exists()

        elif isinstance(obj, Event):
            return obj.calendar.meeting.member_set.filter(user=request.user).exists()

        return False


def is_member(request, obj):
    if isinstance(obj, Meeting):
        return obj.member_set.filter(user=request.user).exists()
    elif isinstance(obj, Member):
        return obj.meeting.member_set.filter(user=request.user).exists()
    elif isinstance(obj, Calendar):
        return obj.meeting.member_set.filter(user=request.user).exists()
    elif isinstance(obj, Event):
        return obj.calendar.meeting.member_set.filter(user=request.user).exists()
    return False

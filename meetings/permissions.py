from rest_framework import permissions
from .models.member import Member


class IsMember(permissions.BasePermission):
    def has_permission(self, request, view, **kwargs):
        if request.user.is_authenticated:
            meeting_id = kwargs.get('meeting_id')
            return Member.objects.filter(user=request.user, meeting_id=meeting_id).exists()
        return False

    # def has_object_permission(self, request, view, obj):
    #     return obj == request.user or request.user.is_staff


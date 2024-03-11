from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser

from ..models.event import Event
from ..models.meeting import Meeting
from ..models.calendar import Calendar
from ..serializer.event_serializer import EventSerializer
from ..permissions import IsMember


@api_view(['GET', 'POST'])
@permission_classes([IsMember | IsAdminUser])
def event_list_view(request, meeting_id, member_id):
    try:
        meeting = Meeting.objects.get(id=meeting_id)
        user = User.objects.get(id=member_id)
        calendar = Calendar.objects.get(meeting=meeting, owner=user)
    except Meeting.DoesNotExist or User.DoesNotExist or Calendar.DoesNotExist:
        return Response({"error": "Couldn't find such calender in database, double check your meeting/member id"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        event = Event.objects.filter(calendar=calendar)
        serializer = EventSerializer(event, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        if request.user == user:
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You do not have permission to perform this action on other user."},
                            status=status.HTTP_403_FORBIDDEN)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsMember | IsAdminUser])
def event_view(request, meeting_id, member_id, event_id):
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({"error": "No such event created"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        meeting = Meeting.objects.get(id=meeting_id)
        user = User.objects.get(id=member_id)
        calendar = Calendar.objects.get(meeting=meeting, owner=user)
    except Meeting.DoesNotExist or User.DoesNotExist or Calendar.DoesNotExist:
        return Response({"error": "Couldn't find such calender in database, double check your meeting/user id"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EventSerializer(event, many=False)
        return Response(serializer.data)
    elif request.method == 'PUT':
        if not Event.objects.filter(calendar=calendar).exists():
            return Response(data={"detail": "Event does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user == user:
            serializer = EventSerializer(event, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You do not have permission to perform this action on other user."},
                            status=status.HTTP_403_FORBIDDEN)
    
    elif request.method == 'DELETE':
        if not Event.objects.filter(calendar=calendar).exists():
            return Response(data={"detail": "Event does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user == user:
            event.delete()
            return Response(data={"detail": "Event deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You do not have permission to perform this action on other user."},
                            status=status.HTTP_403_FORBIDDEN)

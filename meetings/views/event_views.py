from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..models.event import Event
from ..models.calendar import Calendar
from ..serializer import event_serializer
from ..permissions import IsMember

@api_view(['GET', 'POST'])
@permission_classes([IsMember | IsAdminUser])
def event_list_view(request, calendar_id):
    if (request.method == 'GET'):
        event = Event.objects.filter(calendar_id=calendar_id)
        serializer = event_serializer(event, many=True)

        return(serializer.data)
    elif (request.method == 'POST'):
        serializer = event_serializer(request.data)

        if serializer.is_valid():
            serializer.save()

        return(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def event_view(request, meeting_id, member_id, event_id):
    pass

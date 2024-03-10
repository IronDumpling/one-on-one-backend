from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models.calendar import Calendar
from ..serializer.calendar_serializer import CalendarSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calendar_list_view(request, meeting_id):

    # TODO: Query
    calendars = Calendar.objects.filter(meeting = meeting_id)
    if calendars == None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CalendarSerializer(calendars, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST', 'PUT'])
@permission_classes([IsAuthenticated])
def calendar_view(request, meeting_id, member_id):
    # TODO: Query
    calendar = Calendar.objects.get(meeting=meeting_id,owner = member_id)

    if request.method == 'GET':
        serializer = CalendarSerializer(calendar)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = CalendarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    elif request.method == 'PUT':
        serializer = CalendarSerializer(instance=calendar, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import calendar
from ..serializer import calendar_serializer


@api_view(['GET'])
def calendar_list_view(request, meeting_id):
    # TODO: Authentication

    # TODO: Query
    calendars = calendar.Calendar.objects.all()

    if request.method == 'GET':
        serializer = calendar_serializer.CalendarSerializer(calendars, many=True)
        return Response(serializer.data)


@api_view(['GET', 'POST', 'PUT'])
def calendar_view(request, meeting_id, member_id):
    # TODO: Query
    calendars = calendar.Calendar.objects.get(id=meeting_id)

    # TODO: Authentication

    if request.method == 'GET':
        serializer = calendar_serializer.CalendarSerializer(calendars, many=False)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = calendar_serializer.CalendarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        serializer = calendar_serializer.CalendarSerializer(instance=calendars, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

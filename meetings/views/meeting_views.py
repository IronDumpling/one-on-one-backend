from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import meeting
from ..serializer import meeting_serializer


@api_view(['GET', 'POST'])
def meeting_list_view(request):
    meetings = meeting.Meeting.objects.all()

    if request.method == 'GET':
        serializer = meeting_serializer.MeetingSerializer(meetings, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        # TODO: Authentication
        # Add the current user to the meeting
        serializer = meeting_serializer.MeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            # TODO: error handling
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def meeting_view(request, meeting_id):
    meetings = meeting.Meeting.objects.get(id=meeting_id)

    # TODO: Authentication

    if request.method == 'GET':
        serializer = meeting_serializer.MeetingSerializer(meetings, many=False)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = meeting_serializer.MeetingSerializer(instance=meetings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        meetings.delete()
        return None




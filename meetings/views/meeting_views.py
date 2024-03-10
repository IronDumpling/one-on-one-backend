from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models.meeting import Meeting
from ..models.member import Member
from ..serializer import meeting_serializer


@api_view(['GET', 'POST'])
def meeting_list_view(request):

    if request.method == 'GET':
        meetings = Meeting.objects.all()
        serializer = meeting_serializer.MeetingSerializer(meetings, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            serializer = meeting_serializer.MeetingSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                meeting = serializer.save()
                Member.objects.create(meeting=meeting, user=request.user)
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=None, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'PUT', 'DELETE'])
def meeting_view(request, meeting_id):
    meetings = Meeting.objects.get(id=meeting_id)

    # TODO: Authentication

    if request.method == 'GET':
        serializer = meeting_serializer.MeetingSerializer(meetings, many=False)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = meeting_serializer.MeetingSerializer(instance=meetings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        meetings.delete()
        return None




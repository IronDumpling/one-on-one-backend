from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models.meeting import Meeting
from ..models.member import Member
from ..serializer import meeting_serializer


# TODO: Authentication
@api_view(['GET', 'POST'])
def meeting_list_view(request):

    if request.method == 'GET':
        meetings = Meeting.objects.all()
        serializer = meeting_serializer.MeetingSerializer(meetings, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = meeting_serializer.MeetingSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            meeting = serializer.save()
            print("Current request user " + request.user.__str__())
            Member.objects.create(meeting=meeting, user=request.user)
            # TODO: create a join node
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: Authentication
@api_view(['GET', 'PUT', 'DELETE'])
def meeting_view(request, meeting_id):
    meetings = Meeting.objects.get(id=meeting_id)

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
        return Response(None, status=status.HTTP_200_OK)




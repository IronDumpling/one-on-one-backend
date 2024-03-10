from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..models.meeting import Meeting
from ..models.member import Member
from ..serializer import meeting_serializer
from ..permissions import IsMember


@api_view(['GET'])
@permission_classes([IsAdminUser])
def meeting_list_view_get(request):

    meetings = Meeting.objects.all()
    serializer = meeting_serializer.MeetingSerializer(meetings, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def meeting_list_view_post(request):

    serializer = meeting_serializer.MeetingSerializer(data=request.data, partial=True)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    meeting = serializer.save()
    Member.objects.create(meeting=meeting, user=request.user, role='host')
    # TODO: create a join node
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsMember])
def meeting_view(request, meeting_id):
    meetings = Meeting.objects.get(id=meeting_id)

    if request.method == 'GET':
        if meetings is None:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)

        serializer = meeting_serializer.MeetingSerializer(meetings, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = meeting_serializer.MeetingSerializer(instance=meetings, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_205_RESET_CONTENT)

    elif request.method == 'DELETE':
        meetings.delete()
        return Response(None, status=status.HTTP_205_RESET_CONTENT)

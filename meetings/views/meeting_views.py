from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..models.meeting import Meeting
from ..models.member import Member
from ..models.node import JoinNode
from ..serializer import meeting_serializer
from ..permissions import IsMember


class MeetingViewSet(viewsets.ModelViewSet):
    queryset = Meeting.objects.all()
    serializer_class = meeting_serializer.MeetingSerializer

    # @action(detail=False, url_path='', url_name='meeting-list', methods=['GET'])
    def list(self, request, *args, **kwargs):
        self.check_permissions(request)
        return super().list(request, *args, **kwargs)

    # @action(detail=False, url_path='', url_name='meeting-list', methods=['POST'])
    def create(self, request, *args, **kwargs):
        self.check_permissions(request)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        Member.objects.create(meeting=serializer.instance, user=request.user, role='host')
        # TODO Create a join node
        # JoinNode.objects.create()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, url_path='<int:meeting_id>/', url_name='meeting-detail', methods=['GET', 'PUT', 'DELETE'])
    def detail_view(self, request, meeting_id=None):
        meeting = Meeting.objects.get(id=meeting_id)
        if request.method == 'GET':
            if meeting is None:
                return Response(data={"detail": "Meeting does not exist."}, status=status.HTTP_404_NOT_FOUND)
            serializer = meeting_serializer.MeetingSerializer(meeting, many=False)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            serializer = meeting_serializer.MeetingSerializer(instance=meeting, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_205_RESET_CONTENT)

        elif request.method == 'DELETE':
            if not Member.objects.filter(meeting=meeting, user=request.user, role=['host', 'Host']).exists():
                return Response(data={"detail": "You are not the host of the meeting."}, status=status.HTTP_403_FORBIDDEN)
            meeting.delete()
            return Response(data={"detail": "Meeting deleted."}, status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [IsAdminUser]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'detail_view':
            permission_classes = [IsMember | IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

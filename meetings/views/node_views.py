from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from ..models.meeting import Meeting
from ..models.member import Member
from ..models.node import RemindNode, JoinNode, SubmitNode, PollNode, StateNode
from ..serializer.node_serializer import RemindNodeSerializer, JoinNodeSerializer, SubmitNodeSerializer, \
    PollNodeSerializer, StateNodeSerializer, OptionSerializer
from ..permissions import IsMember, is_member


@api_view(['GET'])
@permission_classes([IsMember | IsAdminUser])
def node_list_view(request, meeting_id):
    if not Meeting.objects.filter(id=meeting_id).exists():
        return Response(data={"detail": "Meeting does not exist."},
                        status=status.HTTP_404_NOT_FOUND)

    meeting = Meeting.objects.get(id=meeting_id)
    if not is_member(request, meeting):
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    serializer = {}

    nodes = RemindNode.objects.filter(meeting=meeting)
    serializer.update(RemindNodeSerializer(nodes, many=True).data)
    #
    # nodes = JoinNode.objects.filter(meeting=meeting)
    # serializer.update(JoinNodeSerializer(nodes, many=True).data)
    #
    # nodes = SubmitNode.objects.filter(meeting=meeting)
    # serializer.update(SubmitNodeSerializer(nodes, many=True).data)
    #
    # nodes = PollNode.objects.filter(meeting=meeting)
    # serializer.update(PollNodeSerializer(nodes, many=True).data)
    #
    # nodes = StateNode.objects.filter(meeting=meeting)
    # serializer.update(StateNodeSerializer(nodes, many=True).data)

    sorted_data = sorted(serializer.items(), key=lambda x: x[1]['created_time'])
    sorted_data = dict(sorted_data)

    # TODO: Error when nodes are a lot

    return Response(data=sorted_data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@permission_classes([IsMember | IsAdminUser])
def type_node_list_view(request, meeting_id, node_type):
    if not Meeting.objects.filter(id=meeting_id).exists():
        return Response(data={"detail": "Meeting does not exist."},
                        status=status.HTTP_404_NOT_FOUND)

    meeting = Meeting.objects.get(id=meeting_id)
    if not is_member(request, meeting):
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    if node_type == 'remind' or node_type == 'Remind Node':
        return remind_node_list_view(request, meeting)
    elif node_type == 'join' or node_type == 'Join Node':
        return join_node_list_view(request, meeting)
    elif node_type == 'submit' or node_type == 'Submit Node':
        return submit_node_list_view(request, meeting)
    elif node_type == 'poll' or node_type == 'Poll Node':
        return poll_node_list_view(request, meeting)
    elif node_type == 'state' or node_type == 'State Node':
        return state_node_list_view(request, meeting)
    else:
        return Response(data={'detail': 'The requested node type does not exist.'},
                        status=status.HTTP_404_NOT_FOUND)


def remind_node_list_view(request, meeting):
    if request.method == 'GET':
        nodes = RemindNode.objects.filter(meeting=meeting)
        serializer = RemindNodeSerializer(nodes, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = {
            'meeting': meeting.id,
            'sender': request.user.id,
            **request.data
        }
        data['receiver'] = int(data.get('receiver')[0])
        data['message'] = data.get('message')[0]
        if data['receiver'] and not Member.objects.filter(meeting=meeting, user_id=data['receiver']).exists():
            return Response(data={
                'detail': f"The user with id {data['receiver']} is not a member of the meeting."
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = RemindNodeSerializer(data=data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


def join_node_list_view(request, meeting):
    if request.method == 'GET':
        nodes = JoinNode.objects.filter(meeting=meeting)
        serializer = JoinNodeSerializer(nodes, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = {
            'meeting': meeting.id,
            'sender': request.user.id,
            **request.data
        }
        data['receiver'] = int(data.get('receiver')[0])
        if data['receiver'] and not Member.objects.filter(meeting=meeting, user_id=data['receiver']).exists():
            return Response(data={
                'detail': f"The user with id {data['receiver']} is not a member of the meeting."
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = JoinNodeSerializer(data=data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


def submit_node_list_view(request, meeting):
    if request.method == 'GET':
        nodes = SubmitNode.objects.filter(meeting=meeting)
        serializer = SubmitNodeSerializer(nodes, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = {
            'meeting': meeting.id,
            'sender': request.user.id,
            **request.data
        }

        serializer = SubmitNodeSerializer(data=data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


def poll_node_list_view(request, meeting):
    if request.method == 'GET':
        nodes = PollNode.objects.filter(meeting=meeting)
        serializer = PollNodeSerializer(nodes, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        try:
            options_data = request.data.get('options', [])
        except:
            return Response(data={'detail': 'Missing options field.'}, status=status.HTTP_400_BAD_REQUEST)

        data = {
            'meeting': meeting.id,
            'sender': request.user.id,
        }
        poll_serializer = PollNodeSerializer(data=data)
        if not poll_serializer.is_valid():
            return Response(data=poll_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        poll = poll_serializer.save()

        serializers = [OptionSerializer(data={
            'text': option, 'poll': poll.id
        }) for option in options_data]

        options = [serializer.save() for serializer in serializers if serializer.is_valid()]

        return Response(data={
            'poll': poll_serializer.data,
            'options': [
                serializer.data for serializer in serializers
            ]
        }, status=status.HTTP_201_CREATED)


def state_node_list_view(request, meeting):
    if request.method == 'GET':
        nodes = StateNode.objects.filter(meeting=meeting)
        serializer = StateNodeSerializer(nodes, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = {
            'meeting': meeting.id,
            'sender': request.user.id,
            **request.data
        }

        serializer = StateNodeSerializer(data=data)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT'])
@permission_classes([IsMember | IsAdminUser])
def type_node_view(request, meeting_id, node_type, node_id):
    if not Meeting.objects.filter(id=meeting_id).exists():
        return Response(data={"detail": "Meeting does not exist."},
                        status=status.HTTP_404_NOT_FOUND)

    meeting = Meeting.objects.get(id=meeting_id)
    if not is_member(request, meeting):
        return Response({"detail": "Is not a member."}, status=status.HTTP_403_FORBIDDEN)

    if node_type == 'remind' or node_type == 'Remind Node':
        return remind_node_view(request, meeting, node_id)
    elif node_type == 'join' or node_type == 'Join Node':
        return join_node_view(request, meeting, node_id)
    elif node_type == 'submit' or node_type == 'Submit Node':
        return submit_node_view(request, meeting, node_id)
    elif node_type == 'poll' or node_type == 'Poll Node':
        return poll_node_view(request, meeting, node_id)
    elif node_type == 'state' or node_type == 'State Node':
        return state_node_view(request, meeting, node_id)
    else:
        return Response(data={'detail': 'The requested node type does not exist.'},
                        status=status.HTTP_404_NOT_FOUND)


def remind_node_view(request, meeting, node_id):
    node = RemindNode.objects.get(id=node_id)
    if node is None:
        return Response(data={"detail": "Node does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RemindNodeSerializer(node, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        return Response({"error": "Cannot modify this type of node"}, status=status.HTTP_400_BAD_REQUEST)


def join_node_view(request, meeting, node_id):
    node = JoinNode.objects.get(id=node_id)
    if node is None:
        return Response(data={"detail": "Node does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JoinNodeSerializer(node, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        return Response({"error": "Cannot modify this type of node"}, status=status.HTTP_400_BAD_REQUEST)


def submit_node_view(request, meeting, node_id):
    node = SubmitNode.objects.get(id=node_id)
    if node is None:
        return Response(data={"detail": "Node does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubmitNodeSerializer(node, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        return Response({"error": "Cannot modify this type of node"}, status=status.HTTP_400_BAD_REQUEST)


def poll_node_view(request, meeting, node_id):
    node = PollNode.objects.get(id=node_id)
    if node is None:
        return Response(data={"detail": "Node does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PollNodeSerializer(node, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        try:
            selected_options = request.data.get('selected_options', [])
        except:
            return Response(data={"detail": "Not provide selected option"}, status=status.HTTP_400_BAD_REQUEST)

        for option in selected_options:
            if not node.option_set.filter(text=option).exist():
                return Response(data={'detail': 'Selected option does not exist.'},
                                status=status.HTTP_400_BAD_REQUEST)

        if request.user in node.users_voted.all():
            return Response(data={'detail': 'User has already voted in this poll.'}, status=status.HTTP_400_BAD_REQUEST)

        node.vote(request.user, selected_options)

        members_count = meeting.member_set.count()
        if node.users_voted.count() >= members_count:
            node.state = PollNode.PollState.FINISHED
            meeting.state = Meeting.MeetingState.APPROVING


def state_node_view(request, meeting, node_id):
    node = StateNode.objects.get(id=node_id)
    if node is None:
        return Response(data={"detail": "Node does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StateNodeSerializer(node, many=False)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        return Response({"error": "Cannot modify this type of node"}, status=status.HTTP_400_BAD_REQUEST)

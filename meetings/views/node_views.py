from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from ..models.meeting import Meeting
from ..models.node import RemindNode, JoinNode, SubmitNode, PollNode, StateNode
from ..serializer.node_serializer import RemindNodeSerializer, JoinNodeSerializer, SubmitNodeSerializer, \
    PollNodeSerializer, StateNodeSerializer
from ..permissions import IsMember


@api_view(['GET'])
# @permission_classes([IsMember | IsAdminUser])
def node_list_view(request, meeting_id):
    meeting = Meeting.objects.get(id=meeting_id)
    if meeting is None:
        return Response(data={"detail": "Meeting does not exist."},
                        status=status.HTTP_404_NOT_FOUND)

    serializer = {}

    nodes = RemindNode.objects.filter(meeting=meeting)
    serializer.update(RemindNodeSerializer(nodes, many=True))

    nodes = JoinNode.objects.filter(meeting=meeting)
    serializer.update(JoinNodeSerializer(nodes, many=True))

    nodes = SubmitNode.objects.filter(meeting=meeting)
    serializer.update(SubmitNodeSerializer(nodes, many=True))

    nodes = PollNode.objects.filter(meeting=meeting)
    serializer.update(PollNodeSerializer(nodes, many=True))

    nodes = StateNode.objects.filter(meeting=meeting)
    serializer.update(StateNodeSerializer(nodes, many=True))

    sorted_data = sorted(serializer.items(), key=lambda x: x[1]['created_time'])
    sorted_data = dict(sorted_data)

    return Response(data=sorted_data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
# @permission_classes([IsMember | IsAdminUser])
def type_node_list_view(request, meeting_id, node_type):
    meeting = Meeting.objects.get(id=meeting_id)
    if meeting is None:
        return Response(data={"detail": "Meeting does not exist."},
                        status=status.HTTP_404_NOT_FOUND)

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
        return Response(data=serializer, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        pass


def join_node_list_view(request, meeting):
    if request.method == 'GET':
        nodes = JoinNode.objects.filter(meeting=meeting)
        serializer = JoinNodeSerializer(nodes, many=True)
        return Response(data=serializer, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        pass


def submit_node_list_view(request, meeting):
    if request.method == 'GET':
        nodes = SubmitNode.objects.filter(meeting=meeting)
        serializer = SubmitNodeSerializer(nodes, many=True)
        return Response(data=serializer, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        pass


def poll_node_list_view(request, meeting):
    if request.method == 'GET':
        nodes = PollNode.objects.filter(meeting=meeting)
        serializer = PollNodeSerializer(nodes, many=True)
        return Response(data=serializer, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        pass


def state_node_list_view(request, meeting):
    if request.method == 'GET':
        nodes = StateNode.objects.filter(meeting=meeting)
        serializer = StateNodeSerializer(nodes, many=True)
        return Response(data=serializer, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        pass


@api_view(['GET', 'PUT'])
@permission_classes([IsMember | IsAdminUser])
def type_node_view(request, meeting_id, node_type, node_id):
    meeting = Meeting.objects.get(id=meeting_id)
    if meeting is None:
        return Response(data={"detail": "Meeting does not exist."}, status=status.HTTP_404_NOT_FOUND)

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
        return Response(data=serializer, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        pass


def join_node_view(request, meeting, node_id):
    node = JoinNode.objects.get(id=node_id)
    if node is None:
        return Response(data={"detail": "Node does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JoinNodeSerializer(node, many=False)
        return Response(data=serializer, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        pass


def submit_node_view(request, meeting, node_id):
    node = SubmitNode.objects.get(id=node_id)
    if node is None:
        return Response(data={"detail": "Node does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubmitNodeSerializer(node, many=False)
        return Response(data=serializer, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        pass


def poll_node_view(request, meeting, node_id):
    node = PollNode.objects.get(id=node_id)
    if node is None:
        return Response(data={"detail": "Node does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PollNodeSerializer(node, many=False)
        return Response(data=serializer, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        pass


def state_node_view(request, meeting, node_id):
    node = StateNode.objects.get(id=node_id)
    if node is None:
        return Response(data={"detail": "Node does not exist."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StateNodeSerializer(node, many=False)
        return Response(data=serializer, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        pass

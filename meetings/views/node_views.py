from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def node_list_view(request, meeting_id):
    pass


@api_view(['GET', 'PUT'])
def node_view(request, meeting_id, node_id):
    pass

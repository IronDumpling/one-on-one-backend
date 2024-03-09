from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def event_list_view(request, meeting_id, member_id):
    pass


@api_view(['GET', 'PUT', 'DELETE'])
def event_view(request, meeting_id, member_id, event_id):
    pass

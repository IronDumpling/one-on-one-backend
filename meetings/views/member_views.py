from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# from ..models import
# from ..serializer import meeting_serializer


@api_view(['GET', 'POST'])
def member_list_view(request, meeting_id):
    pass


@api_view(['GET', 'PUT', 'DELETE'])
def member_view(request, meeting_id, member_id):
    pass

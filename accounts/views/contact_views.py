from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def contact_list_view(request, user_id):
    pass


@api_view(['GET', 'PUT', 'DELETE'])
def contact_view(request, user_id, contact_id):
    pass

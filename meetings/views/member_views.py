from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..models import meeting,member
from ..serializer import meeting_serializer,member_serializer




@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def member_list_view(request, meeting_id):

    try:
       Meeting = meeting.objects.get(pk=meeting_id)
    except meeting.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer =meeting_serializer(Meeting)
        return Response(serializer.data)

    elif request.method == 'POST':

        serializer = meeting_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(Meeting=Meeting)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def member_view(request, meeting_id, member_id):
    try:
        Meeting = meeting.objects.get(pk=meeting_id)
    except meeting.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    try:
        Member = member.objects.get(pk=member_id, meeting=meeting)
    except member.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

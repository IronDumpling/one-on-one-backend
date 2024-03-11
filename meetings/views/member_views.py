from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from ..models.node import JoinNode
from ..models.member import Member
from ..permissions import IsMember, is_member
from ..serializer.member_serializer import MemberSerializer
from accounts.models.contact import Contact


@api_view(['GET'])
@permission_classes([IsMember | IsAdminUser])
def member_list_view(request, meeting_id):
    
    members = Member.objects.filter(meeting=meeting_id)

    if not is_member(request, members):
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    if not members:
        return Response({"error": "Members does not exist."}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE', 'POST'])
@permission_classes([IsMember | IsAdminUser])
def member_view(request, meeting_id, user_id):
    if not Member.objects.filter(user=user_id, meeting=meeting_id).exists():
        return Response(data={"detail": "You do not have permission to perform this action."}, status=status.HTTP_404_NOT_FOUND)

    member = Member.objects.get(user=user_id, meeting=meeting_id)
    if not is_member(request, member):
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        try:
            serializer = MemberSerializer(member)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Member.DoesNotExist:
            return Response({"error": "Member is not in meeting."}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PUT':
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':

        if not Member.objects.filter(meeting=meeting_id, user=request.user, role=['host', 'Host']).exists():
            return Response(data={"detail": "You are not the host of the meeting."}, status=status.HTTP_403_FORBIDDEN)
        try:
            member.delete()
            return Response({"Delete success"}, status=status.HTTP_204_NO_CONTENT)
        except Member.DoesNotExist:
            return Response({"error": "Member is not in meeting."}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        # Check if the user is in contact with all users in the meeting
        user = request.user
        # Check if the requesting user is in the meeting
        if Contact.objects.filter(user1=user, user2=user_id).exists():
            member = Member.objects.create(meeting_id=meeting_id, user_id=user_id)
            serializer = MemberSerializer(member)
            JoinNode.objects.create(receiver=user_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Member is not in contact with the requesting user."},
                            status=status.HTTP_403_FORBIDDEN)


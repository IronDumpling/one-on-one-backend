from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models.member import Member
from ..permissions import IsMember
from ..serializer.member_serializer import MemberSerializer
from accounts.models.contact import Contact
from accounts.models.contact import get_contact


@api_view(['GET', 'POST'])
# @permission_classes([IsMember])
def member_list_view(request, meeting_id):
    members = Member.objects.filter(meeting=meeting_id)
    if members is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MemberSerializer(members, many=True)
        return Response(serializer.data)

    # elif request.method == 'POST':

    #     serializer = MemberSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE','POST'])
# @permission_classes([IsMember])
def member_view(request, meeting_id, member_id):

    if request.method == 'GET':
        try: 
            member = Member.objects.get(user=member_id, meeting=meeting_id)
            serializer = MemberSerializer(member)
            return Response(serializer.data)
        except:
            return Response({"error": "Member is not in meeting."},status=status.HTTP_404_NOT_FOUND)


    elif request.method == 'PUT':

        member = Member.objects.get(user=member_id, meeting=meeting_id)
        if member is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = MemberSerializer(member, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        try: 
            member = Member.objects.get(user=member_id, meeting=meeting_id)
            member.delete()
            return Response({"Delete success"},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({"error": "Member is not in meeting."},status=status.HTTP_404_NOT_FOUND)


    elif request.method == 'POST':
        # Check if the user is in contact with all users in the meeting
        user = request.user
        # Check if the requesting user is in the meeting
        if Contact.objects.filter(user1=user, user2=member_id).exists():
            member = Member.objects.create(meeting_id=meeting_id, user_id=member_id)
            serializer = MemberSerializer(member)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Member is not in contact with the requesting user."}, status=status.HTTP_403_FORBIDDEN)





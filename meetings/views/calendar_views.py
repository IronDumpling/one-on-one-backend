from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..permissions import IsMember

from ..models.calendar import Calendar
from ..serializer.calendar_serializer import CalendarSerializer
from ..models.member import Member
from ..models.member import Meeting
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User




def check_all_members_have_calendar(meeting_id):

    meeting = Meeting.objects.get(pk=meeting_id)
    members = Member.objects.filter(meeting=meeting)
    if members.count() <= 2:
        return False, "The meeting does not have more than 2 members."
    calendars = Calendar.objects.filter(meeting=meeting)
    calendar_owner_ids = calendars.values_list('owner', flat=True)
    for member in members:
        if member.user.id not in calendar_owner_ids:
            return False
    return True, "All members have a calendar and the meeting has more than 2 members."
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def calendar_list_view(request, meeting_id):


    calendars = Calendar.objects.filter(meeting = meeting_id)
    if not calendars:
        return Response(data={"detail": "The meeting is null."},status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        calendars = Calendar.objects.filter(meeting = meeting_id)
        serializer = CalendarSerializer(calendars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'PUT'])
# @permission_classes([IsMember])
def calendar_view(request, meeting_id, user_id):

    if not Member.objects.filter(meeting=meeting_id, user=request.user).exists():
        return Response(data={"detail": "You are not the member of the meeting."}, status=status.HTTP_403_FORBIDDEN) 


    if request.method == 'GET':

        try:
            meeting = Meeting.objects.get(id=meeting_id)
        except Meeting.DoesNotExist:
            return Response(data={"detail": "This meeeting is not exist."},status=status.HTTP_404_NOT_FOUND)
        
        try:
            member = Member.objects.get(meeting=meeting_id,user = user_id)
        except Member.DoesNotExist:
            return Response(data={"detail": "Not a member."},status=status.HTTP_404_NOT_FOUND)
        
        try:
            calendar = Calendar.objects.get(meeting=meeting_id,owner = user_id)
            serializer = CalendarSerializer(calendar)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Calendar.DoesNotExist:
            return Response(data={"detail": "This member have not created a calendar."},status=status.HTTP_404_NOT_FOUND)
        


    elif request.method == 'POST':

        if Calendar.objects.filter(meeting=meeting_id, owner=request.user).exists():
            return Response(data={"detail": "You have created a calendar."}, status=status.HTTP_403_FORBIDDEN)
        
        if not Member.objects.filter(meeting=meeting_id, user=request.user).exists():
            return Response(data={"detail": "You are not in the meeting."}, status=status.HTTP_403_FORBIDDEN)
        
        user = request.user

        if user.id != user_id:
            return Response(data={"detail": "You are not the owner."}, status=status.HTTP_404_NOT_FOUND)
        
        calendar = Calendar.objects.create(meeting_id=meeting_id, owner=user)
        serializer = CalendarSerializer(calendar)

        if check_all_members_have_calendar(meeting_id):
            try:
                # 尝试获取ID为-1的用户
                user = User.objects.get(id=-1)
            except ObjectDoesNotExist:
                print("User with ID -1 does not exist.")


            calendar = Calendar.objects.create(meeting_id=meeting_id, owner=user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#check if all the members have created calendar
    
        



    elif request.method == 'PUT':

        user = request.user

        if user.id != user_id:
            return Response(data={"detail": "You are not the owner."}, status=status.HTTP_404_NOT_FOUND)
        calendar = Calendar.objects.get(meeting_id=meeting_id, owner=user)
        if calendar is None:
            return Response(data={"detail": "You have not created the calendar."},status=status.HTTP_404_NOT_FOUND)
        
        serializer = CalendarSerializer(instance=calendar, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

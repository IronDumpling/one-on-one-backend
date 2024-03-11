from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.http import JsonResponse, Http404
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from ..models.event import Event
from ..models.meeting import Meeting
from ..models.calendar import Calendar
from ..serializer.event_serializer import EventSerializer
from ..permissions import IsMember, is_member


def find_intersection(curr_inter, new_inter):
    
    if len(curr_inter) == 0 or len(new_inter) == 0:
        return []
    
    i,j = 0,0
    intersection = []
    while i < len(curr_inter) and j < len(new_inter):

        start1, end1 = curr_inter[i]
        start2, end2 = new_inter[j]

        if start1 <= end2 and start2 <= end1:
            intersection.append((max(start1,start2),min(end1,end2)))

        if end1 < end2:
            i = i + 1
        else:
            j = j + 1

    return intersection
    
        


def get_available_time_intersection(meeting_id):
    calendars_raw = Calendar.objects.filter(meeting_id=meeting_id).exclude(owner__isnull=True)
    
    calendars = []
    for index in range(len(calendars_raw)):
        calendar = calendars_raw[index]
        events = Event.objects.filter(calendar=calendar, availability=Event.Availability.AVAILABLE).order_by('start_time')
        calendars.append([])
        for event in events:
            calendars[index].append((event.start_time, event.end_time))
    
    curr_calendar = calendars[0]
    for calendar in calendars[1:]:
        curr_intersection = find_intersection(curr_calendar,calendar)
        if len(curr_intersection) == 0:
            return []
    
    return curr_intersection




@api_view(['GET', 'POST'])

@permission_classes([IsMember | IsAdminUser])

def event_list_view(request, meeting_id, user_id):
    try:
        meeting = Meeting.objects.get(id=meeting_id)
        user = User.objects.get(id=user_id)
        calendar = Calendar.objects.get(meeting=meeting, owner=user)
    except:
        return Response({"error": "Couldn't find such calender in database, double check your meeting/member id"},
                        status=status.HTTP_404_NOT_FOUND)

    if not is_member(request, meeting) or not is_member(request, calendar):
        return Response({"detail": "You do not have permission to perform this action."},
                        status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        event = Event.objects.filter(calendar=calendar)
        serializer = EventSerializer(event, many=True)

        return Response(serializer.data)
    elif request.method == 'POST':
        if request.user == user:
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                if Calendar.objects.filter(meeting=meeting, owner__isnull=True).exists():
                    null_owner_calendar = Calendar.objects.get(meeting_id=meeting_id, owner__isnull=True)
                    curr_intersection = get_available_time_intersection(meeting_id)
                    curr_intersection_cleaned = []
                    for i, (start_time, end_time) in enumerate(curr_intersection):
                        is_duplicate = any(
                            start_time == later_start and end_time == later_end
                            for later_start, later_end in curr_intersection[i+1:]
                        )
                        if not is_duplicate:
                            curr_intersection_cleaned.append((start_time, end_time))
                    for start_time, end_time in curr_intersection_cleaned:
                        print(f"Start time: {start_time}, End time: {end_time}")
                        event = Event.objects.create(
                                name = 'final decision',
                                calendar=null_owner_calendar,
                                availability=Event.Availability.AVAILABLE,
                                start_time=start_time,
                                end_time=end_time,
                        )
                        event.save()

                        meeting = Meeting.objects.get(id=meeting_id)
                        meeting.state = Meeting.MeetingState.READY
                        meeting.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You do not have permission to perform this action on other user."},
                            status=status.HTTP_403_FORBIDDEN)

@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])

@permission_classes([IsMember | IsAdminUser])
def event_view(request, meeting_id, user_id, event_id):

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({"error": "No such event created"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        meeting = Meeting.objects.get(id=meeting_id)
        user = User.objects.get(id=user_id)
        calendar = Calendar.objects.get(meeting=meeting, owner=user)
    except:
        return Response({"error": "Couldn't find such calender in database, double check your meeting/user id"}, status=status.HTTP_404_NOT_FOUND)

    if not is_member(request, meeting) or not is_member(request, calendar):
        return Response({"detail": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = EventSerializer(event, many=False)
        return Response(serializer.data)
    elif request.method == 'PUT':
        if not Event.objects.filter(calendar=calendar).exists():
            return Response(data={"detail": "Event does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user == user:
            serializer = EventSerializer(event, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You do not have permission to perform this action on other user."},
                            status=status.HTTP_403_FORBIDDEN)
    
    elif request.method == 'DELETE':
        if not Event.objects.filter(calendar=calendar).exists():
            return Response(data={"detail": "Event does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        if request.user == user:
            event.delete()
            return Response(data={"detail": "Event deleted."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You do not have permission to perform this action on other user."},
                            status=status.HTTP_403_FORBIDDEN)

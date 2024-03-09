from django.urls import path
from .views import meeting_views, calendar_views, member_views, node_views, event_views

app_name = 'meetings'

urlpatterns = [
    path('', meeting_views.meeting_list_view, name="meeting_list"),
    path('<int:meeting_id>/', meeting_views.meeting_view, name="meeting"),

    path('<int:meeting_id>/members/', member_views.member_list_view, name="member_list"),
    path('<int:meeting_id>/members/<int:member_id>/', member_views.member_view, name="member"),

    path('<int:meeting_id>/calendars/', calendar_views.calendar_list_view, name="calendar-list"),
    path('<int:meeting_id>/members/<int:member_id>/calendar/', calendar_views.calendar_view, name="calendar"),

    path('<int:meeting_id>/members/<int:member_id>/calendar/events/', event_views.event_list_view, name="event-list"),
    path('<int:meeting_id>/members/<int:member_id>/calendar/events/<int:event_id>/', event_views.event_view, name="event"),

    path('<int:meeting_id>/nodes/', node_views.node_list_view, name="node-list"),
    path('<int:meeting_id>/nodes/<int:node_id>/', node_views.node_view, name="node"),
]

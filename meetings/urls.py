from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import meeting_views, calendar_views, member_views, node_views, event_views

app_name = 'meetings'

router = DefaultRouter()
router.register(r'', meeting_views.MeetingViewSet, basename='meeting')

urlpatterns = [
    path('', include(router.urls)),

    path('<int:meeting_id>/members/', member_views.member_list_view, name="member_list"),
    path('<int:meeting_id>/members/<int:user_id>/', member_views.member_view, name="member"),

    path('<int:meeting_id>/calendars/', calendar_views.calendar_list_view, name="calendar-list"),
    path('<int:meeting_id>/members/<int:user_id>/calendar/', calendar_views.calendar_view, name="calendar"),

    path('<int:meeting_id>/members/<int:user_id>/calendar/events/', event_views.event_list_view, name="event-list"),
    path('<int:meeting_id>/members/<int:user_id>/calendar/events/<int:event_id>/', event_views.event_view, name="event"),

    path('<int:meeting_id>/nodes/', node_views.node_list_view, name="node-list"),
    path('<int:meeting_id>/nodes/<int:node_id>/', node_views.node_view, name="node"),
]

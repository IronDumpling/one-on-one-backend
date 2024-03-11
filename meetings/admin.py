from django.contrib import admin
from .models import calendar, event, meeting, member, node

# Register your models here.
admin.site.register(calendar.Calendar)
admin.site.register(event.Event)
admin.site.register(meeting.Meeting)
admin.site.register(member.Member)
admin.site.register(node.RemindNode)
admin.site.register(node.JoinNode)
admin.site.register(node.SubmitNode)
admin.site.register(node.PollNode)
admin.site.register(node.StateNode)


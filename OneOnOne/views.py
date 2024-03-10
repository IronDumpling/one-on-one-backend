from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Account Register': '/api/accounts/register/',

        'Account Login': '/api/token/',
        'Account Login Refresh': '/api/token/refresh/',

        'Accounts List': '/api/accounts/',
        'Account Detail': '/api/accounts/profile/',

        'Contacts List': '/api/accounts/contacts/',
        'Contacts Detail': '/api/accounts/contacts/<int:contact_id>/',

        'Meeting List': '/api/meetings/',
        'Meeting Detail': '/api/meetings/<int:meeting_id>/',

        'Member List': '/api/meetings/<int:meeting_id>/members/',
        'Member Detail': '/api/meetings/<int:meeting_id>/members/<int:member_id>/',

        'Calendar List': '/api/meetings/<int:meeting_id>/calendars/',
        'Calendar Detail': '/api/meetings/<int:meeting_id>/members/<int:member_id>/calendar/'
    }
    return Response(data=api_urls, status=status.HTTP_200_OK)
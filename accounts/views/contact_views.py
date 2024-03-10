from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializer.contact_serializer import ContactSerializer
from django.db import models
from ..models.contact import Contact

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def contact_list_view(request):
    match request.method:
        case 'GET':
            user = request.user
            print('current_user: ' + user.__str__())
            contacts = Contact.objects.filter(models.Q(user1=user) | models.Q(user2=user))
            serializer = ContactSerializer(contacts, many=True)
            return Response(serializer.data)
        case 'POST':
            data = request.data.copy()
            data.update({'user1': request.user.id})

            serializer = ContactSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def contact_view(request, user_id, contact_id):
    pass

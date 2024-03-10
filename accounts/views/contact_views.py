from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from ..serializer.contact_serializer import ContactSerializer
from django.db import models
from ..models.contact import Contact, get_contact
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

@api_view(['GET', 'POST', "DELETE"])
@permission_classes([IsAuthenticated])
def contact_list_view(request):
    match request.method:
        case 'GET':
            user = request.user
            contacts = Contact.objects.filter(models.Q(user1=user) | models.Q(user2=user))
            serializer = ContactSerializer(contacts, many=True)
            return Response(serializer.data)
        case 'POST':
            data = request.data.copy()
            data.update({'user1': request.user.id})

            user1 = request.user
            user2_id = data.get('user2')

            if str(user1.id) == str(user2_id):
                return Response({"error": "Cannot add yourself as contact."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user2 = User.objects.get(pk=user2_id)
            except User.DoesNotExist:
                return Response({"error": "User2 does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            if get_contact(user1, user2):
                return Response({"error": "Contact already exists."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = ContactSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        case "DELETE":
            user2_id = request.data.get('user2')
            user1 = request.user

            try:
                user2 = User.objects.get(pk=user2_id)
            except User.DoesNotExist:
                return Response({"error": "User2 does not exist."}, status=status.HTTP_400_BAD_REQUEST)

            contact = get_contact(user1, user2)
            if contact:
                contact.delete()
                return Response({"message": "Contact deleted successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Contact does not exist."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def contact_view(request, contact_id):
    contact = get_object_or_404(Contact, pk=contact_id)

    if request.user not in [contact.user1, contact.user2]:
        return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

    match request.method:
        case "GET":
            serializer = ContactSerializer(contact)
            return Response(serializer.data)

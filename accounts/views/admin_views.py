# views.py
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from ..serializer.user_serializer import UserSerializer
from django.contrib.auth.hashers import make_password

@api_view(['GET'])
@permission_classes([IsAdminUser])
def users_view(_):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    try:
        user = User.objects.create_user(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password']
        )
        user.save()
        return Response({"message": "Register success."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile_view(request):
    match request.method:
        case 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        case 'PUT':
            user = request.user
            data = request.data

            if 'email' in data and data['email'] is not None:
                user.email = data['email']

            if 'password' in data and data['password'] is not None:
                user.password = make_password(data['password'])

            user.save()

            # Return the updated user data
            serializer = UserSerializer(user)
            return Response({'message: Update Profile success'}, status=status.HTTP_200_OK)

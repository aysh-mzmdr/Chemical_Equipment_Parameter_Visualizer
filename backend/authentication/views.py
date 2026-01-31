from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer=UserSerializer(data=request.data)

    if serializer.is_valid():
        user=serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username=request.data.get('username')
    password=request.data.get('password')

    user=authenticate(username=username,password=password)

    if user is not None:
        token,_=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user':{
                'username':user.username,
                'first_name':user.first_name,
                'last_name':user.last_name,
                'email':user.email,
                'role':user.profile.role,
                'company':user.profile.company
            }
        },status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.auth.delete()
    return Response(status=status.HTTP_200_OK)
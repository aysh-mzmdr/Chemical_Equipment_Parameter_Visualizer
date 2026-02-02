import pandas as pd
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status

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

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update(request):
    user=request.user
    if user.check_password(request.data.get('currentPassword')):
        user.username=request.data.get('email')
        user.first_name=request.data.get('first_name')
        user.last_name=request.data.get('last_name')
        user.email=request.data.get('email')
        user.profile.role=request.data.get('role')
        user.profile.company=request.data.get('company')
        if request.data.get('newPassword') != '':
            user.set_password(request.data.get('newPassword'))
        user.save()
        user.profile.save()
        return Response(status=status.HTTP_202_ACCEPTED)
    
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class EquipmentUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Read CSV with Pandas
            df = pd.read_csv(file_obj)
            
            # Normalize column names to lower case to avoid case-sensitivity issues
            df.columns = df.columns.str.strip().str.lower()
            
            # 2. Calculate Basic Stats
            total_count = len(df)
            averages = {
                "flowrate": round(df['flowrate'].mean(), 2),
                "pressure": round(df['pressure'].mean(), 2),
                "temperature": round(df['temperature'].mean(), 2)
            }

            # 3. Calculate Distribution (for Charts)
            # Returns: {'Pump': 10, 'Valve': 5, ...}
            type_counts = df['type'].value_counts().to_dict()
            
            # Structure for Chart.js/Matplotlib
            chart_data = {
                "labels": list(type_counts.keys()),
                "values": list(type_counts.values())
            }

            return Response({
                "total_count": total_count,
                "averages": averages,
                "distribution": chart_data,
                "message": "Analysis Complete"
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
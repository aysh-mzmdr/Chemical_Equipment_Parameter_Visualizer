import pandas as pd
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from .models import Record
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny

class EquipmentUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

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

            resultData={
                "total_count": total_count,
                "averages": averages,
                "distribution": chart_data,
            }
            Record.objects.create(user=request.user,data=resultData)
            # 3. Enforce Limit (Keep only last 5)
            # Logic: Get IDs of the newest 5 records. Delete anything NOT in that list.
            user_records = Record.objects.filter(user=request.user)
            last_five_ids = user_records.order_by('-created_at').values_list('id', flat=True)[:5]
            # Delete records belonging to THIS user that are NOT in the top 5
            user_records.exclude(id__in=last_five_ids).delete()
            
            return Response(resultData, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def record(request):
    user = request.user
    
    # 1. Fetch records for the current user, newest first
    records = Record.objects.filter(user=user).order_by('-created_at')
    # 2. Check if empty
    if not records.exists():
        return Response({"resultData": None}, status=status.HTTP_200_OK)
    
    # 3. Serialize the data
    # We extract the 'data' field (which contains your averages, charts, etc.) 
    # and optionally add the timestamp so the frontend knows when it happened.
    history_list = []
    for record in records:
        record_entry = record.data # This is the JSON dict saved earlier
        record_entry['created_at'] = record.created_at # Add timestamp for UI display
        history_list.append(record_entry)
        
    return Response({"resultData": history_list}, status=status.HTTP_200_OK)
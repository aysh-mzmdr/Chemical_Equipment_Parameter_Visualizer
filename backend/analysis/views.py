import pandas as pd
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response

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
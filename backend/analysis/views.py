import pandas as pd
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.response import Response
from .models import Record
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated

import io
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pypdf import PdfReader, PdfWriter # For password protection
from django.http import HttpResponse

class EquipmentUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 1. Read CSV
            df = pd.read_csv(file_obj)
            df.columns = df.columns.str.strip().str.lower()
            
            # 2. Calculate Stats
            total_count = len(df)
            averages = {
                "flowrate": round(df['flowrate'].mean(), 2) if not df.empty else 0,
                "pressure": round(df['pressure'].mean(), 2) if not df.empty else 0,
                "temperature": round(df['temperature'].mean(), 2) if not df.empty else 0
            }

            type_counts = df['type'].value_counts().to_dict()
            chart_data = {
                "labels": list(type_counts.keys()),
                "values": list(type_counts.values())
            }

            # 3. Create Data Dict (WITHOUT created_at yet)
            resultData = {
                "total_count": total_count,
                "averages": averages,
                "distribution": chart_data,
            }

            # 4. Save to Database FIRST
            # We assign it to 'new_record' so we can access its properties
            new_record = Record.objects.create(user=request.user, data=resultData)

            # 5. Add Timestamp to Response
            # Now we can get the real time from the DB and add it to the result
            resultData['created_at'] = new_record.created_at

            # 6. Enforce Limit (Keep only last 5)
            user_records = Record.objects.filter(user=request.user)
            last_five_ids = user_records.order_by('-created_at').values_list('id', flat=True)[:5]
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def download(request):
    try:
        # 1. Get Data from Frontend
        chart_image_b64 = request.data.get('chartImage') # Base64 string
        stats = request.data.get('stats')
        created_at = request.data.get('created_at')

        # 2. Create the PDF in memory
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # --- PDF CONTENT DESIGN ---
        p.setFont("Helvetica-Bold", 18)
        p.drawString(50, height - 50, "Equipment Analysis Report")
        
        p.setFont("Helvetica", 12)
        p.drawString(50, height - 80, f"Date: {created_at}")
        p.drawString(50, height - 100, f"Generated for: {request.user.email}")

        # Draw Stats Text
        y_position = height - 150
        p.drawString(50, y_position, "Summary Statistics:")
        y_position -= 20
        p.setFont("Courier", 12)
        
        if stats:
            for key, value in stats.items():
                p.drawString(70, y_position, f"{key.capitalize()}: {value}")
                y_position -= 20

        # Draw Chart Image (Decode Base64)
        if chart_image_b64:
            try:
                # Remove header "data:image/png;base64," if present
                if "base64," in chart_image_b64:
                    chart_image_b64 = chart_image_b64.split("base64,")[1]
                
                image_data = base64.b64decode(chart_image_b64)
                image_stream = io.BytesIO(image_data)
                from reportlab.lib.utils import ImageReader
                img = ImageReader(image_stream)
                
                # Draw image (x, y, width, height)
                p.drawImage(img, 50, y_position - 300, width=400, height=250)
            except Exception as e:
                print(f"Image Error: {e}")

        p.showPage()
        p.save()
        buffer.seek(0)

        # 3. Add Password Protection (User Email)
        input_pdf = PdfReader(buffer)
        output_pdf = PdfWriter()
        
        for page in input_pdf.pages:
            output_pdf.add_page(page)
            
        # Encrypt with User Email
        password = request.user.email
        output_pdf.encrypt(password)
        
        # 4. Return as File Response
        final_buffer = io.BytesIO()
        output_pdf.write(final_buffer)
        final_buffer.seek(0)
        
        filename = f"{created_at.replace(':', '-').replace(' ', '_')}.pdf"
        response = HttpResponse(final_buffer, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
        return response

    except Exception as e:
        return Response({"error": str(e)}, status=500)
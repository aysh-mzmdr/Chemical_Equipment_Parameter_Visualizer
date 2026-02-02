from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', EquipmentUploadView.as_view(), name='upload-csv'),
    path('record/',record,name='record')
]
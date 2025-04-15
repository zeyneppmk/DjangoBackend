from django.urls import path
from .views import UploadAndTranscribeView, TranscribeResultView

urlpatterns = [
    path('upload/', UploadAndTranscribeView.as_view(), name='upload-and-transcribe'),
    path('result/', TranscribeResultView.as_view(), name='transcribe-result'),
]

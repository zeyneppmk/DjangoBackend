from django.urls import path
from .views import AudioUploadAndTranscribeView, AdminAudioFileListView

urlpatterns = [
    path('upload/', AudioUploadAndTranscribeView.as_view(), name='audio-upload'),
    path('admin-processed-files/', AdminAudioFileListView.as_view(), name='admin-processed-files')
]


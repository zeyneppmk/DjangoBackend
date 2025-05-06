from django.urls import path
from .views import AudioUploadAndTranscribeView, AudioFileDeleteView, AdminAudioFileListView

urlpatterns = [
    path('upload/', AudioUploadAndTranscribeView.as_view(), name='audio-upload'),
    path('delete/<int:pk>/', AudioFileDeleteView.as_view(), name='audio-delete'),
    path('admin-processed-files/', AdminAudioFileListView.as_view(), name='admin-processed-files'),
]



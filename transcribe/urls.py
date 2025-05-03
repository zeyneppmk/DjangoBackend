from django.urls import path
from .views import AudioUploadAndTranscribeView, AudioFileDeleteView

urlpatterns = [
    path('upload/', AudioUploadAndTranscribeView.as_view(), name='audio-upload'),
    path('delete/<int:pk>/', AudioFileDeleteView.as_view(), name='audio-delete')
]



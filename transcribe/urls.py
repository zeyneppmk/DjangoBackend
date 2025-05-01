from django.urls import path
from .views import AudioUploadAndTranscribeView

urlpatterns = [
    path('upload/', AudioUploadAndTranscribeView.as_view(), name='audio-upload'),
]



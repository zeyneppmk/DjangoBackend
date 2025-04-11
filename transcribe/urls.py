from django.urls import path
from .views import TranscribeResultView

urlpatterns = [
    path('transcribe/', TranscribeResultView.as_view(), name='transcribe-upload'),
]

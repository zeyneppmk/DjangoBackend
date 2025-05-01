import requests
import os
import httpx
import uuid 
import asyncio

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from .serializers import AudioFileSerializer
from .models import AudioFile, TranscriptionSummary, TranscriptSegment
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .utils import upload_to_cloudinary, send_audio_to_fastapi

User = get_user_model()

class AudioUploadAndTranscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if not file:
            return Response({"error": "Ses dosyası bulunamadı."}, status=status.HTTP_400_BAD_REQUEST)

        filename = f"{uuid.uuid4().hex}_{file.name}"
        temp_audio_path = f"temp/{filename}"

        os.makedirs(os.path.dirname(temp_audio_path), exist_ok=True)

        with open(temp_audio_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # FastAPI'ye dosyayı gönder
        fastapi_response = asyncio.run(send_audio_to_fastapi(temp_audio_path))

        result = fastapi_response["results"][0]
        segments = result.get("transcript")
        summary = result.get("summary")

        # Ses dosyasını Cloudinary'ye yükle
        audio_url = upload_to_cloudinary(temp_audio_path)

        # Veritabanına AudioFile kaydet
        audio_file = AudioFile.objects.create(
            user=request.user,
            filename=file.name,
            content=audio_url
        )

        # Veritabanına TranscriptSegment kaydet
        for idx, segment in enumerate(segments):
            TranscriptSegment.objects.create(
                audio_file=audio_file,
                speaker=segment['speaker'],
                start_time=segment['start'],
                end_time=segment['end'],
                text=segment['text'],
                order=idx
            )

        # Veritabanına TranscriptionSummary kaydet
        TranscriptionSummary.objects.create(
            audio_file=audio_file,
            summary_text=summary
        )

        # Geçici dosyaları temizle
        os.remove(temp_audio_path)

        # AudioFile'ı serialize ederek frontend'e göster
        serializer = AudioFileSerializer(audio_file, context={'request': request})

        return Response({
            "message": "Dosya başarıyla yüklendi ve işlendi.",
            "audio_file": serializer.data
        }, status=status.HTTP_201_CREATED)
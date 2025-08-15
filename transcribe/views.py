import requests
import os
import httpx
import uuid 
import asyncio
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .serializers import AudioFileSerializer,AudioFileAdminSerializer 
from .models import AudioFile, TranscriptionSummary, TranscriptSegment
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .utils import upload_to_cloudinary, send_audio_to_fastapi, generate_pdf, upload_pdf_to_cloudinary

User = get_user_model()

class AudioUploadAndTranscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        #ses dosyasının reacttan alınması
        file = request.FILES.get('file') 

        if not file:
            return Response({"error": "Ses dosyası bulunamadı."}, status=status.HTTP_400_BAD_REQUEST)
        #geçiçi dosyaya kaydetme
        filename = f"{uuid.uuid4().hex}_{file.name}"
        temp_audio_path = f"temp/{filename}"

        os.makedirs(os.path.dirname(temp_audio_path), exist_ok=True)

        with open(temp_audio_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        # FastAPI'ye gönderilen dosyasnın json verisinin fastapi_response atanması
        fastapi_response = asyncio.run(send_audio_to_fastapi(temp_audio_path))

        #json dosyasının resulta atanması , dictionary yapısı
        result = fastapi_response["results"][0]
        #konuşma segmentleri
        segments = result.get("transcript", [])
        #özet
        summary = result.get("summary","")

        # Ses dosyasını Cloudinary'ye yükle
        audio_url = upload_to_cloudinary(temp_audio_path)

        # Veritabanına AudioFile kaydet
        audio_file = AudioFile.objects.create(
            user=request.user,
            filename=file.name,
            content=audio_url
        )

        # Segmentleri kaydet
        full_text = ""
        for idx, segment in enumerate(segments):
            TranscriptSegment.objects.create(
                audio_file=audio_file,
                speaker=segment['speaker'],
                text=segment['text'],
                order=idx,
                start_time=segment.get("start", 0.0),
                end_time=segment.get("end", 0.0)
            )
            full_text += segment["text"] + "\n"

        # Veritabanına TranscriptionSummary kaydet
        TranscriptionSummary.objects.create(
            audio_file=audio_file,
            summary_text=summary
        )

        # PDF üret ve yükle
        transcript_pdf_path = generate_pdf(segments, "Transkript",is_summary=False)
        summary_pdf_path = generate_pdf(summary, "Özet", is_summary=True)

        transcript_pdf_url = upload_pdf_to_cloudinary(transcript_pdf_path)
        summary_pdf_url = upload_pdf_to_cloudinary(summary_pdf_path)

        audio_file.transcript_pdf_url = transcript_pdf_url
        audio_file.summary_pdf_url = summary_pdf_url
        audio_file.save()           

        # Geçici dosyaları temizle
        os.remove(temp_audio_path)
        os.remove(transcript_pdf_path)
        os.remove(summary_pdf_path)
        
        # AudioFile'ı serialize ederek frontend'e göster
        serializer = AudioFileSerializer(audio_file, context={'request': request})

        return Response({
            "message": "Dosya başarıyla yüklendi ve işlendi.",
            "audio_file": serializer.data
        }, status=status.HTTP_201_CREATED)
    
class AdminAudioFileListView(generics.ListAPIView):
    serializer_class = AudioFileAdminSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return AudioFile.objects.prefetch_related("segments", "summary").order_by("-uploaded_at")
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import status
import requests
import os
from django.core.files.storage import default_storage
from .serializers import AudioFileSerializer
from .models import AudioFile, TranscriptionSummary, TranscriptSegment
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

User = get_user_model()

class TranscribeResultView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("👤 Gelen user:", request.user)
        print("🛡 Authenticated?", request.user.is_authenticated)
        print("✅ TranscribeResultView tetiklendi:", request.user)
        try:
            result = request.data['results'][0]

            data = {
                'filename': result['filename'],
                'audio_url': result['filename'],
                'segments': [
                    {
                        "speaker": seg["speaker"],
                        "start_time": seg["start"],
                        "end_time": seg["end"],
                        "text": seg["text"]
                    } for seg in result['transcript']
                ]
            }

            serializer = AudioFileSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                audio_file = serializer.save()

                TranscriptionSummary.objects.create(
                    audio_file=audio_file,
                    summary_text=result['summary']
                )

                return Response({"detail": "Transcription and summary saved!"}, status=status.HTTP_201_CREATED)
            else:
                print("❌ Serializer Hataları:", serializer.errors)  # ← buraya
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UploadAndTranscribeView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file_obj = request.FILES.get('file')

        if not file_obj:
            return Response({"error": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        file_path = default_storage.save(file_obj.name, file_obj)
        abs_file_path = os.path.join(default_storage.location, file_path)

        with open(abs_file_path, 'rb') as f:
            files = [('files', (file_obj.name, f, 'audio/wav'))]
            try:
                response = requests.post('http://localhost:8001/transcribe/', files=files)
                if response.status_code != 200:
                    return Response({"error": "FastAPI error", "detail": response.text}, status=500)

                result = response.json()['results'][0]

                data = {
                    'filename': result['filename'],
                    'audio_url': result['filename'],
                    'segments': [
                        {
                            "speaker": seg["speaker"],
                            "start_time": seg["start"],
                            "end_time": seg["end"],
                            "text": seg["text"]
                        } for seg in result['transcript']
                    ]
                }

                serializer = AudioFileSerializer(data=data, context={'request': request})
                if serializer.is_valid():
                    audio_file = serializer.save()
                    TranscriptionSummary.objects.create(
                        audio_file=audio_file,
                        summary_text=result['summary']
                    )
                    return Response({"detail": "Uploaded, transcribed and saved."}, status=201)
                else:
                    return Response(serializer.errors, status=400)

            except Exception as e:
                return Response({"error": str(e)}, status=500)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def whoami(request):
    return Response({"user": request.user.username})
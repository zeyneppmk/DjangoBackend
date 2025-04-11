from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AudioFileSerializer
from .models import TranscriptionSummary

class TranscribeResultView(APIView):
    def post(self, request):
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

                # Summary kaydı
                TranscriptionSummary.objects.create(
                    audio_file=audio_file,
                    summary_text=result['summary']
                )

                return Response({"detail": "Transcription and summary saved!"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

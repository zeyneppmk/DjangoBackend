from rest_framework import serializers
from .models import AudioFile, TranscriptSegment, TranscriptionSummary

class TranscriptSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptSegment
        fields = ['speaker', 'start_time', 'end_time', 'text', 'order']
        read_only_fields = ['order']

class TranscriptionSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptionSummary
        fields = ['summary_text']

class AudioFileSerializer(serializers.ModelSerializer):
    segments = TranscriptSegmentSerializer(many=True, write_only=True)
    summary = TranscriptionSummarySerializer(read_only=True)

    class Meta:
        model = AudioFile
        fields = ['id', 'filename', 'content', 'uploaded_at', 'segments', 'summary']
        read_only_fields = ['uploaded_at', 'content', 'id']

    def create(self, validated_data):
        segments_data = validated_data.pop('segments')
        request = self.context.get("request")
        user = request.user if request and request.user.is_authenticated else None

        if not user:
            raise serializers.ValidationError("Kullanıcı doğrulaması başarısız.")
    
        # Cloudinary yükleme ve content URL'si burada ayarlanacak (views içinde halledeceğiz)

        audio_file = AudioFile.objects.create(user=user, **validated_data)
        for idx, segment in enumerate(segments_data):
            TranscriptSegment.objects.create(audio_file=audio_file, order=idx, **segment)

        return audio_file




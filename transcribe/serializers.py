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
    segments = TranscriptSegmentSerializer(many=True, read_only=True)
    summary = TranscriptionSummarySerializer(read_only=True)
    transcript_pdf_url = serializers.URLField(read_only=True)
    summary_pdf_url = serializers.URLField(read_only=True)

    class Meta:
        model = AudioFile
        fields = ['id', 'filename', 'content', 'uploaded_at', 'segments', 'summary','transcript_pdf_url', 'summary_pdf_url']
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
    

    # admin görünümüne uygun sade serializer'lar

from rest_framework import serializers
from .models import AudioFile, TranscriptSegment, TranscriptionSummary


class TranscriptSegmentAdminSerializer(serializers.ModelSerializer):
    audio_file = serializers.StringRelatedField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = TranscriptSegment
        fields = ['id', 'audio_file', 'user', 'speaker', 'start_time', 'end_time']

    def get_user(self, obj):
        return obj.audio_file.user.username


class TranscriptionSummaryAdminSerializer(serializers.ModelSerializer):
    audio_file = serializers.StringRelatedField()
    user = serializers.SerializerMethodField()
    summary_text = serializers.SerializerMethodField()

    class Meta:
        model = TranscriptionSummary
        fields = ['id', 'audio_file', 'user', 'summary_text']

    def get_user(self, obj):
        return obj.audio_file.user.username

    def get_summary_text(self, obj):
        return "🔒 Gizli içerik"


class AudioFileAdminSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    segments = TranscriptSegmentAdminSerializer(many=True, read_only=True)
    summary = TranscriptionSummaryAdminSerializer(read_only=True)

    class Meta:
        model = AudioFile
        fields = ['id', 'filename', 'user', 'uploaded_at', 'segments', 'summary']





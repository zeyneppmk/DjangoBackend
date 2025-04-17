from rest_framework import serializers
from .models import AudioFile, TranscriptSegment, TranscriptionSummary

class TranscriptSegmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptSegment
        fields = ['speaker', 'start_time', 'end_time', 'text', 'order']


class AudioFileSerializer(serializers.ModelSerializer):
    segments = TranscriptSegmentSerializer(many=True, write_only=True)

    class Meta:
        model = AudioFile
        fields = ['filename', 'audio_url', 'segments']

    def create(self, validated_data):
        segments_data = validated_data.pop('segments')
        request = self.context.get("request")
        user = request.user if request and request.user.is_authenticated else None

        if not user:
            username = request.data.get('username') if request else None
        from users.models import CustomUser
        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Kullanıcı bulunamadı.")

        audio_file = AudioFile.objects.create(user=user, **validated_data)
        for idx, segment in enumerate(segments_data):
            TranscriptSegment.objects.create(audio_file=audio_file, order=idx, **segment)

        return audio_file


class TranscriptionSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptionSummary
        fields = ['summary_text']

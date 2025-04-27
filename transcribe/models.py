from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AudioFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content = models.URLField()
   

    def __str__(self):
        return self.filename


class TranscriptSegment(models.Model):
    audio_file = models.ForeignKey(AudioFile, related_name="segments", on_delete=models.CASCADE)
    speaker = models.CharField(max_length=50)
    start_time = models.FloatField()
    end_time = models.FloatField()
    text = models.TextField()
    order = models.IntegerField()

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.audio_file.filename}_transcript"
    
    @classmethod
    def get_full_transcript(cls, audio_file):
        segments = cls.objects.filter(audio_file=audio_file).order_by('order')
        full_text = " ".join(segment.text for segment in segments)
        return full_text

class TranscriptionSummary(models.Model):
    audio_file = models.OneToOneField(AudioFile, on_delete=models.CASCADE, related_name='summary')
    summary_text = models.TextField()

    def __str__(self):
        return f"{self.audio_file.filename}_summary"

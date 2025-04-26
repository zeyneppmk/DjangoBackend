from django.contrib import admin
from .models import AudioFile, TranscriptSegment, TranscriptionSummary

@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'user', 'uploaded_at')
    list_filter = ('uploaded_at', 'user')
    search_fields = ('filename', 'user__username')

@admin.register(TranscriptSegment)
class TranscriptSegmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'audio_file', 'speaker', 'start_time', 'end_time')
    list_filter = ('speaker',)
    search_fields = ('text',)

@admin.register(TranscriptionSummary)
class TranscriptionSummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'audio_file', 'summary_text')
    search_fields = ('summary_text',)
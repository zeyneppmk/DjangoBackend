from django.contrib import admin
from .models import AudioFile, TranscriptSegment, TranscriptionSummary

@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'filename', 'user', 'uploaded_at')
    list_filter = ('uploaded_at', 'user')
    search_fields = ('filename', 'user__username')

@admin.register(TranscriptSegment)
class TranscriptSegmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'audio_file', 'get_user','speaker', 'start_time', 'end_time')
    list_filter = ('speaker',)
    search_fields = ('text',)

    def get_user(self, obj):
        return obj.audio_file.user
    get_user.short_description = 'User'
    get_user.admin_order_field = 'audio_file__user'

@admin.register(TranscriptionSummary)
class TranscriptionSummaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'audio_file', 'get_user', 'get_summary_placeholder')
    search_fields = ('summary_text',)

    def get_user(self, obj):
        return obj.audio_file.user
    get_user.short_description = 'User'
    get_user.admin_order_field = 'audio_file__user'

    def get_summary_placeholder(self, obj):
        return "🔒 Gizli içerik"
    get_summary_placeholder.short_description = "Summary Text"
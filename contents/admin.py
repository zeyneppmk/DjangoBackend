from django.contrib import admin
from .models import BlogContent, HomeContent, ServicesContent
from django.utils.html import format_html

@admin.register(BlogContent)
class BlogContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'image_tag')  # image_tag gösterilecek sütun
    search_fields = ('title', 'content')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "—"
    image_tag.short_description = "Görsel"

@admin.register(HomeContent)
class HomeContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type', 'created_at', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100"/>', obj.image.url)
        return "-"
    image_tag.short_description = 'Görsel'

@admin.register(ServicesContent)
class ServicescontentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
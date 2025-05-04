from django.db import models

class BlogContent(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.title


class HomeContent(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('hero', 'Hero'),
        ('card', 'Kart'),
        ('tech', 'Teknoloji')
    ]

    type = models.CharField(max_length=10, choices=CONTENT_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='home_images/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.type} - {self.title}"



class ServicesContent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.title
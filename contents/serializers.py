from rest_framework import serializers
from .models import BlogContent, HomeContent, ServicesContent
from users.models import CustomUser

class BlogContentSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = BlogContent
        fields = ['id', 'title', 'content', 'link', 'image', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    joined = serializers.DateTimeField(source='date_joined', format="%Y-%m-%d %H:%M")

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'joined']

class HomeContentSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    image = serializers.ImageField(write_only=True, required=False)  

    class Meta:
        model = HomeContent
        fields = ['id', 'title', 'description', 'type', 'image_url', 'image'] 

    def get_image_url(self, obj): 
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class ServicesContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServicesContent
        fields = '_all_'
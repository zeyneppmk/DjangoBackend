from django.shortcuts import render
from rest_framework.permissions import AllowAny

from rest_framework import generics, permissions
from .models import Blog
from users.models import CustomUser
from .serializers import BlogSerializer, UserSerializer
from rest_framework.permissions import IsAdminUser

from rest_framework.views import APIView
from rest_framework.response import Response

class TestView(APIView):
    permission_classes = [AllowAny]  
    def get(self, request):
        return Response({"message": "AdminPanel API çalışıyor!"})


# Kullanıcıları Listele
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

# Kullanıcı Sil
class UserDeleteView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

# Blog Listele ve Ekle
class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all().order_by('-created_at')
    serializer_class = BlogSerializer
    permission_classes = [IsAdminUser]

# Blog Sil ve Güncelle
class BlogRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAdminUser]

from django.shortcuts import render
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import viewsets, generics, permissions
from .models import BlogContent, HomeContent, ServicesContent
from .serializers import BlogContentSerializer, HomeContentSerializer, ServicesContentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser

class TestView(APIView):
    permission_classes = [AllowAny]  
    def get(self, request):
        return Response({"message": "AdminPanel API çalışıyor!"})

class PublicBlogContentListView(generics.ListAPIView):
    queryset = BlogContent.objects.all().order_by('-created_at')
    serializer_class = BlogContentSerializer
    permission_classes = [permissions.AllowAny]

class BlogContentListCreateView(generics.ListCreateAPIView):
    queryset = BlogContent.objects.all().order_by('-created_at')
    serializer_class = BlogContentSerializer
    permission_classes = [IsAdminUser]

# Blog Sil ve Güncelle
class BlogContentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BlogContent.objects.all()
    serializer_class = BlogContentSerializer
    permission_classes = [IsAdminUser]

class HomeContentViewSet(viewsets.ModelViewSet):
    queryset = HomeContent.objects.all()
    serializer_class = HomeContentSerializer
    parser_classes = [MultiPartParser, FormParser] 
    
    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]
    
    def get_serializer_context(self):
        return {'request': self.request}

class ServicesContentViewSet(viewsets.ModelViewSet):
    queryset = ServicesContent.objects.all()
    serializer_class = ServicesContentSerializer

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]
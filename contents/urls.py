from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import TestView, BlogContentListCreateView, BlogContentRetrieveUpdateDestroyView, PublicBlogContentListView, HomeContentViewSet, ServicesContentViewSet #hasret ekledi

urlpatterns = [
    path('test/', TestView.as_view(), name='adminpanel-test'),

    # Blog
    # Halka açık blog listesi hasret ekledi
    path('blogs/public/', PublicBlogContentListView.as_view(), name='public-blog-list'),
    # Admin için ekleme/silme/güncelleme hasret ekledi
    path('blogs/', BlogContentListCreateView.as_view(), name='admin-blog-list-create'),
    path('blogs/<int:pk>/', BlogContentRetrieveUpdateDestroyView.as_view(), name='adminpanel-blog-detail'),
    
    # Yeni: Home içerikleri (tam kontrol)
    path('home/', HomeContentViewSet.as_view({'get': 'list', 'post': 'create'}), name='home-list-create'),
    path('home/<int:pk>/', HomeContentViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='home-detail'),

    # Yeni: Hizmet içerikleri (tam kontrol)
    path('services/', ServicesContentViewSet.as_view({'get': 'list', 'post': 'create'}), name='services-list-create'),
    path('services/<int:pk>/', ServicesContentViewSet.as_view({'put': 'update', 'delete': 'destroy'}), name='services-detail'),   
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
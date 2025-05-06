from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings 
from django.conf.urls.static import static 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/transcribe/', include('transcribe.urls')), 
    path('api/contents/', include('contents.urls')), #hasret ekledi
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #hasret ekledi
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh') #hasret ekledi
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  #hasret ekledi
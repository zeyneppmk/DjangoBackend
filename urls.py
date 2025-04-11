from django.contrib import admin  # bu satır eksikti
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('transcribe.urls')),
]

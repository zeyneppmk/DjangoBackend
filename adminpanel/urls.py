from django.urls import path
from . import views
from .views import TestView, UserListView, UserDeleteView, BlogListCreateView, BlogRetrieveUpdateDestroyView


urlpatterns = [
     path('test/', TestView.as_view(), name='adminpanel-test'),
    path('users/', UserListView.as_view(), name='adminpanel-user-list'),
    path('users/<int:pk>/', UserDeleteView.as_view(), name='adminpanel-user-delete'),
    path('blogs/', BlogListCreateView.as_view(), name='adminpanel-blog-list-create'),
    path('blogs/<int:pk>/', BlogRetrieveUpdateDestroyView.as_view(), name='adminpanel-blog-detail'),
]

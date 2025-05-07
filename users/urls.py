from django.urls import path
from .views import RegisterView, ProfileView, ChangePasswordView, UserAudioHistoryView, UserListView, UserDeleteView,UserAudioFileDeleteView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="get_token"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("profile/", ProfileView.as_view(), name="user-profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("history/", UserAudioHistoryView.as_view(), name="user-history"),
    path("history/<int:pk>/delete/", UserAudioFileDeleteView.as_view(), name="user-audiofile-delete"),
    path("all-users/", UserListView.as_view(), name="user-list"),
    path("<int:pk>/", UserDeleteView.as_view(), name="user-delete"),
] 

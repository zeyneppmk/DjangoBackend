from rest_framework import generics, permissions, status
from .serializers import RegisterSerializer, ProfileSerializer, ChangePasswordSerializer, UserListSerializer
#Projeye tanımlanmış kullanıcı modelini dinamik olarak getirir (CustomUser)
from django.contrib.auth import get_user_model
#API isteklerine verilecek yanıtları olusturmak
from rest_framework.response import Response
from transcribe.models import AudioFile
from transcribe.serializers import AudioFileSerializer


User = get_user_model()

#kullanıcı kayıt islemi
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny] #herkesin erisebilmesi gerekir cunku kayit ekrani

#profil sayfasini dondurur
class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    #sadece giris yapanlar erisebilir.
    permission_classes = [permissions.IsAuthenticated]

    #sadece kendi profilini(bilgilerinin) getirilmesini sağlar güvenlik acisindan önemlidir
    def get_object(self):
        return self.request.user

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [permissions.IsAuthenticated]

    #sadece kendi sifrenisin getirilmesi icin
    def get_object(self):
        return self.request.user

    def update(self, request,*args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Eski şifre doğru mu kontrol et
            if not self.object.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": "Eski şifre yanlış."}, status=status.HTTP_400_BAD_REQUEST)

            # Yeni şifreyi ayarla
            self.object.set_password(serializer.validated_data['new_password'])
            self.object.save()

            return Response({"detail": "Şifre başarıyla değiştirildi."})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAudioHistoryView(generics.ListAPIView):
    serializer_class = AudioFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AudioFile.objects.filter(user=self.request.user).order_by('-uploaded_at')


class UserAudioFileDeleteView(generics.DestroyAPIView):
    serializer_class = AudioFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AudioFile.objects.filter(user=self.request.user)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAdminUser]  # sadece admin görebilsin istersen

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer 
    permission_classes = [permissions.IsAdminUser]

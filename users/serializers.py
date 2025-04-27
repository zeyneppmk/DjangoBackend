from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken 

#projede olusturulan CustomUser modelini kullanmis oluyorum default olani degildir
User = get_user_model()

#yeni bir kullanici kaydederken kullanilan sinif
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("username","first_name", "last_name", "email", "password", "password2")
        extra_kwargs = {"email": {"required": True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Şifreler eşleşmiyor."})
        
        user = User(username=attrs["username"], email=attrs["email"])

        validate_password(attrs["password"], user=user)
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email","is_staff", "is_superuser")

class ChangePasswordSerializer(serializers.Serializer):
        old_password = serializers.CharField(required=True)
        new_password = serializers.CharField(required=True, validators=[validate_password])
        new_password2 = serializers.CharField(required=True)

        def validate(self, attrs):
            if attrs['new_password'] != attrs['new_password2']:
                raise serializers.ValidationError({"new_password": "Yeni şifreler eşleşmiyor."})
            return attrs

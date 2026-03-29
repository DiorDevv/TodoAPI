from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Todo


class UserSerializer(serializers.ModelSerializer):
    """Foydalanuvchi ma'lumotlari (parol ko'rsatilmaydi)."""

    class Meta:
        model = User
        fields = ["id", "username", "email", "date_joined"]


class RegisterSerializer(serializers.ModelSerializer):
    """Yangi foydalanuvchi ro'yxatdan o'tkazish."""

    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Parollar mos kelmaydi.")
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create_user(**validated_data)
        return user


class TodoSerializer(serializers.ModelSerializer):
    """Todo CRUD uchun asosiy serializer."""

    owner = UserSerializer(read_only=True)  # Faqat o'qish uchun

    class Meta:
        model = Todo
        fields = [
            "id",
            "owner",
            "title",
            "description",
            "is_completed",
            "priority",
            "due_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]

    def create(self, validated_data):
        # owner avtomatik request.user dan olinadi (ViewSet da belgilanadi)
        return super().create(validated_data)

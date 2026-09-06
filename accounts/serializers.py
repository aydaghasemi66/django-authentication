from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import TrainerProfile, StudentProfile

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """مرحله‌ی ۱: فقط ایمیل و پسورد"""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CompleteProfileSerializer(serializers.ModelSerializer):
    """مرحله‌ی ۲: نام، عکس، نقش"""

    class Meta:
        model = User
        fields = ["first_name", "last_name", "photo", "role"]

    def validate_role(self, value):
        if value not in ("student", "trainer"):
            raise serializers.ValidationError("role باید student یا trainer باشه")
        return value

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        # بر اساس role، پروفایل مربوطه رو می‌سازیم (اگه از قبل نساخته)
        if instance.role == "trainer":
            TrainerProfile.objects.get_or_create(user=instance)
        elif instance.role == "student":
            StudentProfile.objects.get_or_create(user=instance)

        instance.save()
        return instance
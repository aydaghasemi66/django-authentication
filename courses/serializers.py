from rest_framework import serializers
from .models import Category, Course, Comment, Reply


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ["id", "name", "message", "created_at"]


class CommentSerializer(serializers.ModelSerializer):
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "name", "email", "message", "created_at", "replies"]
        extra_kwargs = {"email": {"write_only": True}}  # ایمیل تو پاسخ عمومی نمایش داده نشه


class CourseListSerializer(serializers.ModelSerializer):
    """برای لیست دوره‌ها - سبک، بدون description کامل"""
    category = serializers.StringRelatedField()
    trainer_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id", "title", "slug", "category", "trainer_name", "price",
            "image", "counted_views", "counted_likes",
        ]

    def get_trainer_name(self, obj):
        return f"{obj.trainer.user.first_name} {obj.trainer.user.last_name}"


class CourseDetailSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source="category", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    trainer_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            "id", "title", "slug", "category", "category_detail",
            "trainer", "trainer_name", "description", "price", "image",
            "counted_views", "counted_likes", "available_seats",
            "schedule", "status", "created_at", "comments",
        ]
        read_only_fields = ["trainer", "counted_views", "counted_likes"]

    def get_trainer_name(self, obj):
        return f"{obj.trainer.user.first_name} {obj.trainer.user.last_name}"
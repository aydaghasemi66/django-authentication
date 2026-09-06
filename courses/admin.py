from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Course, Comment, Reply


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["title", "trainer", "category", "price", "status", "created_at"]
    list_filter = ["status", "category"]
    search_fields = ["title", "description"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "course", "status", "created_at"]
    list_filter = ["status"]


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ["name", "comment", "status", "created_at"]
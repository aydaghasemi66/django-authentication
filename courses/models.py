from django.db import models

# Create your models here.
from django.db import models
from django.utils.text import slugify
from accounts.models import TrainerProfile


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, related_name="courses"
    )
    trainer = models.ForeignKey(
        TrainerProfile, on_delete=models.CASCADE, related_name="courses"
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to="courses/", null=True, blank=True)

    counted_views = models.PositiveIntegerField(default=0)
    counted_likes = models.PositiveIntegerField(default=0)
    available_seats = models.PositiveIntegerField(default=0)
    schedule = models.DateTimeField(null=True, blank=True)
    status = models.BooleanField(default=False)  # False=پیش‌نویس, True=منتشرشده

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    status = models.BooleanField(default=False)  # نیاز به تایید قبل از نمایش
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} on {self.course.title}"


class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="replies")
    name = models.CharField(max_length=100)
    message = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Reply by {self.name}"
from django.shortcuts import render
from rest_framework.exceptions import PermissionDenied

# Create your views here.
from rest_framework import viewsets, permissions, generics
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Course, Comment
from .serializers import (
    CategorySerializer, CourseListSerializer,
    CourseDetailSerializer, CommentSerializer,
)
from .permissions import IsTrainerOwnerOrReadOnly
from accounts.permissions import IsProfileComplete


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(status=True)
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsTrainerOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return CourseListSerializer
        return CourseDetailSerializer

    def get_permissions(self):
        if self.action == "create":
            return [permissions.IsAuthenticated(), IsProfileComplete()]
        return super().get_permissions()


    def perform_create(self, serializer):
        user = self.request.user
        if not hasattr(user, "trainer_profile"):
            raise PermissionDenied("only trainers can create course")
        serializer.save(trainer=user.trainer_profile)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.counted_views += 1
        instance.save(update_fields=["counted_views"])
        return super().retrieve(request, *args, **kwargs)


class CommentCreateView(generics.CreateAPIView):
    """POST /api/courses/<course_slug>/comments/"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        course = Course.objects.get(slug=self.kwargs["course_slug"])
        serializer.save(course=course, status=False)  # نیاز به تایید ادمین
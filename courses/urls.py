from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, CourseViewSet, CommentCreateView

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("", CourseViewSet, basename="course")

urlpatterns = [
    path("<slug:course_slug>/comments/", CommentCreateView.as_view(), name="course-comments"),
    path("", include(router.urls)),
]
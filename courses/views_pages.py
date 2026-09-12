from django.views.generic import ListView, DetailView
from .models import Course, Category
from django.views.generic import ListView, DetailView, FormView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .forms import CommentForm

class CourseListPageView(ListView):
    model = Course
    template_name = "courses.html"
    context_object_name = "courses"

    def get_queryset(self):
        return Course.objects.filter(status=True).select_related("category", "trainer__user")


class CourseDetailPageView(DetailView):
    model = Course
    template_name = "course-details.html"
    context_object_name = "course"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        return Course.objects.filter(status=True).select_related("category", "trainer__user")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.counted_views += 1
        obj.save(update_fields=["counted_views"])
        return obj


class AddCommentView(FormView):
    form_class = CommentForm
    template_name = "course-details.html"  # فقط برای موقعی که فرم خطا داره لازمه

    def form_valid(self, form):
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        comment = form.save(commit=False)
        comment.course = course
        comment.status = False  # نیاز به تایید ادمین
        comment.save()
        messages.success(self.request, "Your comment has been submitted and is awaiting approval.")
        return redirect("course-detail-page", slug=course.slug)

    def form_invalid(self, form):
        messages.error(self.request, "Please fill in all fields correctly.")
        course = get_object_or_404(Course, slug=self.kwargs["slug"])
        return redirect("course-detail-page", slug=course.slug)
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from courses.views_pages import CourseListPageView, CourseDetailPageView
from accounts.views_pages import TrainerListPageView
from accounts.views_pages import (
    RegisterPageView, CompleteProfilePageView, UserLoginView, UserLogoutView,
)
from courses.views_pages import AddCommentView



urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls")),
    path("api/courses/", include("courses.urls")),
    path("api/orders/", include("order.urls")),

    # صفحات HTML
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("about/", TemplateView.as_view(template_name="about.html"), name="about"),
    path("trainers/", TrainerListPageView.as_view(), name="trainers"),
    path("events/", TemplateView.as_view(template_name="events.html"), name="events"),
    path("pricing/", TemplateView.as_view(template_name="pricing.html"), name="pricing"),
    path("contact/", TemplateView.as_view(template_name="contact.html"), name="contact"),
    path("starter-page/", TemplateView.as_view(template_name="starter-page.html"), name="starter-page"),
    path("register/", RegisterPageView.as_view(), name="register-page"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("complete-profile/", CompleteProfilePageView.as_view(), name="complete-profile-page"),

    path("courses/", CourseListPageView.as_view(), name="courses-page"),
    path("courses/<slug:slug>/", CourseDetailPageView.as_view(), name="course-detail-page"),
    path("courses/<slug:slug>/comment/", AddCommentView.as_view(), name="add-comment-page"),
]
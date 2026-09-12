from django.views.generic import CreateView, UpdateView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegisterForm, CompleteProfileForm
from .models import TrainerProfile, StudentProfile, TrainerProfile
from django.views.generic import ListView, CreateView, UpdateView

class RegisterPageView(CreateView):
    form_class = RegisterForm
    template_name = "register.html"
    success_url = reverse_lazy("complete-profile-page")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # بعد از ثبت‌نام خودکار لاگین کن
        return response


class CompleteProfilePageView(LoginRequiredMixin, UpdateView):
    form_class = CompleteProfileForm
    template_name = "complete-profile.html"
    success_url = reverse_lazy("home")
    login_url = "login"

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        if user.role == "trainer":
            TrainerProfile.objects.get_or_create(user=user)
        elif user.role == "student":
            StudentProfile.objects.get_or_create(user=user)
        return response


class UserLoginView(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        return reverse_lazy("home")


class UserLogoutView(LogoutView):
    next_page = "home"

class TrainerListPageView(ListView):
    model = TrainerProfile
    template_name = "trainers.html"
    context_object_name = "trainers"

    def get_queryset(self):
        return TrainerProfile.objects.select_related("user")
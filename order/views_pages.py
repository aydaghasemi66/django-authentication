from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from courses.models import Course
from .models import Order, OrderItem, Enrollment


class AddToCartView(LoginRequiredMixin, View):
    login_url = "login"

    def post(self, request, slug):
        course = get_object_or_404(Course, slug=slug, status=True)

        if not hasattr(request.user, "student_profile"):
            messages.error(request, "Only students can enroll in courses.")
            return redirect("course-detail-page", slug=slug)

        student = request.user.student_profile

        if Enrollment.objects.filter(student=student, course=course).exists():
            messages.info(request, "You are already enrolled in this course.")
            return redirect("course-detail-page", slug=slug)

        order, _ = Order.objects.get_or_create(student=student, status="pending")
        item, created = OrderItem.objects.get_or_create(
            order=order, course=course, defaults={"price_at_purchase": course.price}
        )
        if created:
            messages.success(request, f"{course.title} added to your cart.")
        else:
            messages.info(request, "This course is already in your cart.")
        return redirect("cart-page")


class RemoveFromCartView(LoginRequiredMixin, View):
    login_url = "login"

    def post(self, request, item_id):
        student = request.user.student_profile
        item = get_object_or_404(
            OrderItem, id=item_id, order__student=student, order__status="pending"
        )
        item.delete()
        messages.success(request, "Item removed from cart.")
        return redirect("cart-page")


class CartPageView(LoginRequiredMixin, TemplateView):
    template_name = "cart.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self.request.user, "student_profile"):
            context["not_student"] = True
            return context
        student = self.request.user.student_profile
        order, _ = Order.objects.get_or_create(student=student, status="pending")
        context["order"] = order
        return context


class MyEnrollmentsPageView(LoginRequiredMixin, TemplateView):
    template_name = "my-enrollments.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not hasattr(self.request.user, "student_profile"):
            context["not_student"] = True
            context["enrollments"] = []
            return context
        student = self.request.user.student_profile
        context["enrollments"] = student.enrollments.select_related("course")
        return context
class CheckoutView(LoginRequiredMixin, View):
    login_url = "login"

    def post(self, request):
        if not hasattr(request.user, "student_profile"):
            messages.error(request, "Only students can checkout.")
            return redirect("cart-page")

        student = request.user.student_profile
        order = get_object_or_404(Order, student=student, status="pending")

        if not order.items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect("cart-page")

        order.status = "paid"
        order.save()
        for item in order.items.all():
            Enrollment.objects.get_or_create(student=student, course=item.course)

        messages.success(request, "Payment successful! You are now enrolled.")
        return redirect("my-enrollments-page")
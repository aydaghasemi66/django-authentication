from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Order, OrderItem, Enrollment
from .serializers import OrderSerializer, AddItemSerializer, EnrollmentSerializer
from .permissions import IsStudent
from courses.models import Course


class OrderListView(generics.ListAPIView):
    """GET /api/orders/  -> سفارش‌های خودم"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Order.objects.filter(student=self.request.user.student_profile)


class OrderDetailView(generics.RetrieveAPIView):
    """GET /api/orders/<id>/"""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Order.objects.filter(student=self.request.user.student_profile)


class AddItemView(APIView):
    """POST /api/orders/add-item/  body: {course_id}"""
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request):
        serializer = AddItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = get_object_or_404(Course, id=serializer.validated_data["course_id"])

        student = request.user.student_profile

        if Enrollment.objects.filter(student=student, course=course).exists():
            return Response(
                {"detail": "شما قبلاً در این دوره ثبت‌نام کرده‌اید."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order, _ = Order.objects.get_or_create(student=student, status="pending")

        item, created = OrderItem.objects.get_or_create(
            order=order, course=course,
            defaults={"price_at_purchase": course.price},
        )
        if not created:
            return Response(
                {"detail": "این دوره از قبل در سبد شما هست."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class CheckoutView(APIView):
    """
    POST /api/orders/<id>/checkout/
    فعلاً پرداخت واقعی نداریم، فقط status رو paid می‌کنیم
    و Enrollment برای هر آیتم می‌سازیم.
    """
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request, pk):
        order = get_object_or_404(
            Order, pk=pk, student=request.user.student_profile, status="pending"
        )

        if not order.items.exists():
            return Response(
                {"detail": "سبد خرید خالی است."}, status=status.HTTP_400_BAD_REQUEST
            )

        order.status = "paid"
        order.save()

        for item in order.items.all():
            Enrollment.objects.get_or_create(student=order.student, course=item.course)

        return Response(OrderSerializer(order).data)


class MyEnrollmentsView(generics.ListAPIView):
    """GET /api/orders/my-enrollments/"""
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user.student_profile)
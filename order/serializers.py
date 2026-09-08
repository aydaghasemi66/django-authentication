from rest_framework import serializers
from .models import Order, OrderItem, Enrollment
from courses.models import Course


class OrderItemSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "course", "course_title", "price_at_purchase"]
        read_only_fields = ["price_at_purchase"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "status", "items", "total_price", "created_at"]


class AddItemSerializer(serializers.Serializer):
    course_id = serializers.IntegerField()

    def validate_course_id(self, value):
        if not Course.objects.filter(id=value, status=True).exists():
            raise serializers.ValidationError("دوره‌ی معتبری با این شناسه پیدا نشد.")
        return value


class EnrollmentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Enrollment
        fields = ["id", "course", "course_title", "enrolled_at"]
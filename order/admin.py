from django.contrib import admin

from .models import Order, OrderItem, Enrollment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "student", "status", "total_price", "created_at"]
    list_filter = ["status"]
    inlines = [OrderItemInline]


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ["student", "course", "enrolled_at"]
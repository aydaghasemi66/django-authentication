from django.contrib import admin
from .models import User, OtpCode

# ثبت مدل User در Admin
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone_number", "full_name", "is_active", "is_admin")
    search_fields = ("email", "phone_number")
    list_filter = ("is_active", "is_admin")

admin.site.register(User, UserAdmin)

# ثبت مدل OtpCode در Admin
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "code", "created_at")
    search_fields = ("phone_number", "code")
    list_filter = ("created_at",)

admin.site.register(OtpCode, OtpCodeAdmin)

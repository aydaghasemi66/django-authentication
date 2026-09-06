from rest_framework.permissions import BasePermission


class IsProfileComplete(BasePermission):
    """
    فقط به کاربرهایی که پروفایلشون (نام و نقش) کامله اجازه می‌ده.
    برای مسیرهایی مثل enroll شدن تو کورس، ساختن کورس (اگه trainer) و غیره استفاده می‌شه.
    """
    message = "you should first complete your profile"

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_profile_complete
        )
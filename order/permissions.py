from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    message = "این عملیات فقط برای دانشجویان مجاز است."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "student_profile")
        )
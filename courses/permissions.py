from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsTrainerOwnerOrReadOnly(BasePermission):
    """
    هرکسی می‌تونه بخونه (GET).
    فقط trainer صاحب دوره می‌تونه ویرایش/حذف کنه.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return (
            hasattr(request.user, "trainer_profile")
            and obj.trainer == request.user.trainer_profile
        )
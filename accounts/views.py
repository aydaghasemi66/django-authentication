from rest_framework import generics, permissions
from .serializers import RegisterSerializer, CompleteProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class CompleteProfileView(generics.UpdateAPIView):
    """PATCH /api/auth/complete-profile/  """
    serializer_class = CompleteProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user




class MeView(APIView):
    """GET /api/auth/me/  -> اطلاعات کاربر لاگین‌شده + وضعیت پروفایل"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "is_profile_complete": user.is_profile_complete,
        })
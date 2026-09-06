from rest_framework import generics, permissions
from .serializers import RegisterSerializer, CompleteProfileSerializer


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
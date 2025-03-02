from django.core.mail import send_mail
from django.utils import timezone
from random import randint
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ...models import OtpCode

class SendOtpView(APIView):
    def post(self, request):
        email = request.data.get("email")
        phone_number = request.data.get("phone_number")

        if not email and not phone_number:
            return Response({"error": "Email or Phone Number is required."}, status=status.HTTP_400_BAD_REQUEST)

        otp_code = randint(100000, 999999)  

        if email:
            try:
                send_mail(
                    'Your OTP Code',
                    f'Your OTP code is: {otp_code}',
                    'no-reply@example.com',  
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                return Response({"error": f"Failed to send email: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if phone_number:
           
            pass

   
        OtpCode.objects.filter(phone_number=phone_number).delete()

        OtpCode.objects.create(
            phone_number=phone_number,
            code=otp_code,
            created_at=timezone.now()
        )

        return Response({"message": "OTP sent successfully!"}, status=status.HTTP_200_OK)

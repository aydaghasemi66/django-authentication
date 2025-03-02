from django.urls import path
from .views import SendOtpView

urlpatterns = [
    path('send-otp/', SendOtpView.as_view(), name='send_otp'),
]

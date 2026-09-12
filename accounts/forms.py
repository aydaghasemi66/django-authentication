from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["email"]


class CompleteProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "photo", "role"]
        widgets = {
            "role": forms.Select(choices=User.ROLE_CHOICES),
        }
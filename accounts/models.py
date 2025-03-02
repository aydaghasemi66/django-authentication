from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, full_name, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not phone_number:
            raise ValueError("User must have a phone number")
        
        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            full_name=full_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, full_name, password):
        user = self.create_user(email, phone_number, full_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name="Email Address",
        max_length=255,
        unique=True,
    )
    phone_number = models.CharField(max_length=11, unique=True)
    full_name = models.CharField(max_length=255)
    is_phone_verified = models.BooleanField(default=False)  
    
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone_number", "full_name"]
    
    def __str__(self) -> str:
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
    def get_full_name(self):
        return self.full_name
    
    def get_short_name(self):
        return self.full_name.split()[0] if " " in self.full_name else self.full_name


class OtpCode(models.Model):
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True) 
    code = models.IntegerField()
    created_at = models.DateTimeField()

    def __str__(self):
        return f"OTP Code: {self.code} for {self.email or self.phone_number}"

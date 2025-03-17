# from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
# from django.db import models
# from django.utils import timezone
#
# class CustomUserManager(UserManager):
#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError('The email must be set')
#
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#
#         return user
#
#     def create_user(self, email=None, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)
#
#
#     def create_superuser(self, email=None, password=None, ** extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self._create_user(email, password, **extra_fields)
#
# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(blank=True, default='', unique=True)
#     name = models.CharField( max_length=255,  blank=True,default='')
#
#     is_active = models.BooleanField(default=True)
#     is_superuser= models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#
#     date_joined = models.DateTimeField(default=timezone.now)
#     last_login = models.DateTimeField(blank=True, null=True)
#
#     objects = CustomUserManager()
#
#     USERNAME_FIELD = 'email'
#     EMAIL_FIELDS = 'email'
#     REQUIRED_FIELDS = []
#
#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'
#
#     def get_full_name(self):
#         return self.name
#
#     def get_short_name(self):
#         return self.name or self.email.split('@')[0]
#
#
# from django.db import models
# from django.utils.translation import gettext_lazy as _
# from django.contrib.auth import get_user_model
#
# class Role(models.Model):
#     class RoleChoices(models.TextChoices):
#         USER = "user", _("Обычный пользователь")
#         ADMIN = "admin", _("Админ")
#         SUPERADMIN = "superadmin", _("Суперадмин")
#
#     user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="role")
#     role = models.CharField(max_length=20, choices=RoleChoices.choices, default=RoleChoices.USER)
#
#     def __str__(self):
#         return f"{self.user.email} - {self.role}"

from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Role(models.Model):
    class RoleChoices(models.TextChoices):
        USER = "user", _("Обычный пользователь")
        ADMIN = "admin", _("Админ")
        SUPERADMIN = "superadmin", _("Суперадмин")

    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="role")
    role = models.CharField(max_length=20, choices=RoleChoices.choices, default=RoleChoices.USER)

    def __str__(self):
        return f"{self.user.email} - {self.role}"



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255, blank=True, default="")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

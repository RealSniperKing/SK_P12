from django.db import models
import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models import ForeignKey
from django.contrib.auth.models import Group

# class CustomPermission(models.Model):
#     class Types(models.TextChoices):
#         MANAGEMENT = '0', 'Management'
#         SALES = '1', 'Sales'
#         SUPPORT = '2', 'Support'
#         CLIENT = '3', 'Client'
#
#     role_permission = models.CharField(max_length=64, choices=Types.choices, default=Types.CLIENT)
#
#     def __str__(self):
#         return self.role_permission


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Vous devez saisir un email")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email=email, password=password)
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user

def getGroupNames():
    print("------------ getGroupNames ------------")
    groups = Group.objects.all().values_list('name', flat=True)
    print(groups)
    return zip(groups, groups)

class User(AbstractBaseUser, PermissionsMixin):
    # Required fields
    email = models.EmailField(unique=True, max_length=255, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    # Optional fields
    # ROLE_CHOICES = (
    #     ('0', 'Management'),
    #     ('1', 'Sales'),
    #     ('2', 'Support'),
    #     ('3', 'Client')
    # )
    class Types(models.TextChoices):
        # def __init__(self):

        MANAGEMENT = '0', 'Management'
        SALES = '1', 'Sales'
        SUPPORT = '2', 'Support'
        CLIENT = '3', 'Client'

    print(getGroupNames())
    role = models.CharField(max_length=64, choices=getGroupNames(), default=Types.CLIENT)

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []  # Email & Password are required by default

    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.email
from django.db import models
import uuid
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import Group

from rest_framework.exceptions import ValidationError


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
    groups = Group.objects.all().values_list('name', flat=True)
    return zip(groups, groups)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    user_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Types(models.TextChoices):
        MANAGEMENT = '0', 'Management'
        SALES = '1', 'Sales'
        SUPPORT = '2', 'Support'
        CLIENT = '3', 'Client'

    role = models.CharField(max_length=64, choices=getGroupNames(), blank=True)

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


class ManagementGroupName(models.Model):
    name = models.CharField(max_length=200, blank=False)

    def save(self, *args, **kwargs):
        if not self.pk and ManagementGroupName.objects.exists():
            # if you'll not check for self.pk, then error will also raised in update of exists model
            raise ValidationError('There is can be only one ManagementGroupName instance')
        return super(ManagementGroupName, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Management group name"

    def __str__(self):
        return self.name

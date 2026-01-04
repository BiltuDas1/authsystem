import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
  def create_user(self, email: str, password, **extra_info):
    if not email:
      raise ValueError("`email` is a required field")
    user = Users(email=email.lower(), **extra_info)
    user.set_password(password)
    user.save()
    return user

class Users(AbstractBaseUser):
  id = models.UUIDField(
    primary_key=True,
    default=uuid.uuid4,
    editable=False
  )
  firstname = models.CharField(max_length=100)
  lastname = models.CharField(max_length=100)
  email = models.EmailField(unique=True, max_length=255)

  class Role(models.TextChoices):
    ADMIN = 'ADMIN', 'Admin'
    USER = 'USER', 'User'

  role = models.CharField(
    max_length=5,
    choices=Role.choices,
    default=Role.USER
  )

  is_active = models.BooleanField(default=False)

  # Custom Manager
  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['firstname', 'lastname']

class EmailVerify(models.Model):
  id = models.OneToOneField(
    Users,
    on_delete=models.CASCADE,
    primary_key=True
  )
  token = models.CharField(max_length=64, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)

class ResetEmailVerify(models.Model):
  user = models.ForeignKey(
    Users,
    on_delete=models.CASCADE
  )
  token = models.CharField(max_length=64, unique=True)
  created_at = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=True)
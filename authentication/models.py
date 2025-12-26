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

  is_active = models.BooleanField(default=True)

  # Custom Manager
  objects = UserManager()

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['firstname', 'lastname']
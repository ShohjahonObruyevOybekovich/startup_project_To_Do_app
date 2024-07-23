import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from account.managers import UserManager

class CustomUser(AbstractUser):
    username = None
    uuid = models.UUIDField(unique=True,editable=False,default=uuid.uuid4)
    email = models.EmailField(max_length=100, blank=True, unique=True)
    full_name = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='media/profile_pics/', null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True, unique=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now=True, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    objects = UserManager()


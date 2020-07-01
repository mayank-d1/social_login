from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=50, null=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True, db_index=True)
    meta = JSONField(null=True)

    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = "user"
        verbose_name = "User"
        verbose_name_plural = "Users"

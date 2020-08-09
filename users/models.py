import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    active = models.BooleanField(blank=True, null=True, default=False)

    def __str__(self):
        return self.username

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=200)

    def _str_(self):
        return self.username
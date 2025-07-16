from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    address = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.username
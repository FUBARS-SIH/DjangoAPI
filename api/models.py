from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.dispatch import receiver

class CustomUser(AbstractUser):
    is_authority = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

class Authority(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    district = models.CharField(max_length=200)

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.district)

class Reporter(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    school_name = models.CharField(max_length=250)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.school_name)

from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.db.models.functions import Now
from django.contrib.postgres.fields import JSONField

class CustomUser(AbstractUser):
    is_authority = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.username

class Authority(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    district = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.district)

class School(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    school_name = models.CharField(max_length=250, blank=False)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.school_name)

class Report(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, unique_for_date="reported_for_date")

    reported_student_count = models.PositiveIntegerField(blank=False)
    reported_menu = JSONField()
    reported_for_date = models.DateField('date reported for', blank=False)
    reported_on_datetime = models.DateTimeField('date and time reported on', default=Now())

    estimated_student_count = models.PositiveIntegerField()
    estimated_menu = JSONField()
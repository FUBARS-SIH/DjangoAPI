from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.db.models.functions import Now
from django.contrib.postgres.fields import JSONField


class CustomUser(AbstractUser):
    email = models.EmailField(blank=False, unique=True)
    is_authority = models.BooleanField(default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class District(models.Model):
    name = models.CharField(max_length=200, blank=False, unique=True)


class Authority(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    district = models.OneToOneField(District, on_delete=models.PROTECT)

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.district.name)


class School(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=250, blank=False)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True)
    authority = models.ForeignKey(
        Authority, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.name)


class Report(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    student_count = models.PositiveIntegerField(blank=False)
    for_date = models.DateField('date reported for', blank=False)
    on_datetime = models.DateTimeField(
        'date and time reported on', auto_now_add=True)
    actual_report = models.OneToOneField('self', related_name='estimate_report', on_delete=models.CASCADE, null=True, blank=True)
    added_by_school = models.BooleanField(default=False)

    def __str__(self):
        report_type = 'Actual report' if self.added_by_school == True else 'Estimate report'
        return '{} - {} - {}'.format(self.school_id, self.for_date, report_type)

    class Meta:
        unique_together = ('school', 'for_date', 'added_by_school')


class ReportItem(models.Model):
    report = models.ForeignKey(Report, related_name='items', on_delete=models.CASCADE)
    item = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return '{} - {}'.format(self.report_id, self.item)

    class Meta:
        unique_together = ('report', 'item')


class Schedule(models.Model):
    district = models.ForeignKey(District, on_delete=models.PROTECT)
    days = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday')
    )
    day = models.IntegerField(choices=days)
    item = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return '{}'.format(self.district)
    
    class Meta:
        unique_together = ('district', 'day')
        

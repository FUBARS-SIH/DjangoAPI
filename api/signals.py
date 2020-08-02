from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Report, AuthorityReport

@receiver(post_save, sender=Report)
def create_authority_report(sender, instance, created, **kwargs):
    try:
        # create authority report only when both actual and estimate report exists
        other_report = Report.objects.get(school=instance.school, for_date=instance.for_date, added_by_school=(not instance.added_by_school))

        if instance.added_by_school:
            AuthorityReport.objects.create(school=instance.school, actual=instance, estimate=other_report, for_date=instance.for_date)
        else:
            AuthorityReport.objects.create(school=instance.school, estimate=instance, actual=other_report, for_date=instance.for_date)

    except Report.DoesNotExist:
        pass

@receiver(post_save, sender=AuthorityReport)
def send_discrepancy_email(sender, instance, created, **kwargs):
    if instance.is_discrepant:
        # TODO: send email to authority
        pass
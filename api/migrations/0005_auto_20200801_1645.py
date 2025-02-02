# Generated by Django 3.0.8 on 2020-08-01 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20200729_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='added_by_school',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='report',
            unique_together={('school', 'for_date', 'added_by_school')},
        ),
    ]

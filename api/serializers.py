from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import CustomUser, Authority, School, Report, District, ReportItem
from collections import OrderedDict
from django.core.exceptions import ValidationError
from django.db import transaction


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        fields = [
            'id',
            'username',
            'email',
            'password',
            'is_authority',
        ]


class ReportItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportItem
        fields = [
            'item',
        ]


class SchoolReportSerializer(serializers.ModelSerializer):
    items = ReportItemSerializer(many=True)

    class Meta:
        model = Report
        fields = [
            'id',
            'student_count',
            'for_date',
            'items',
        ]

    @transaction.atomic
    def create(self, validateddata):
        itemsdata = validateddata.pop('items')
        report = Report.objects.create(**validateddata)
        for itemdata in itemsdata:
            ReportItem.objects.create(report=report, **itemdata)
        return report

    @transaction.atomic
    def update(self, instance, validateddata):
        itemsdata = validateddata.pop('items')
        for attr, value in validateddata.items():
            setattr(instance, attr, value)
        if itemsdata:
            instance.items.all().delete()
            for itemdata in itemsdata:
                ReportItem.objects.create(report=instance, **itemdata)
        instance.save()
        return instance


class EstimatedReportSerializer(serializers.ModelSerializer):
    items = ReportItemSerializer(many=True)

    class Meta:
        model = Report
        fields = [
            'id',
            'student_count',
            'for_date',
            'items',
        ]

    @transaction.atomic
    def create(self, validateddata):
        itemsdata = validateddata.pop('items')
        school = validateddata.get('school')
        for_date = validateddata.get('for_date')
        actual_report = Report.objects.get(school=school, for_date=for_date)
        report = Report.objects.create(actual_report=actual_report, **validateddata)
        for itemdata in itemsdata:
            ReportItem.objects.create(report=report, **itemdata)
        return report

    @transaction.atomic
    def update(self, instance, validateddata):
        itemsdata = validateddata.pop('items')
        for attr, value in validateddata.items():
            setattr(instance, attr, value)
        if itemsdata:
            instance.items.all().delete()
            for itemdata in itemsdata:
                ReportItem.objects.create(report=instance, **itemdata)
        instance.save()
        return instance

class AuthoritySerializer(serializers.ModelSerializer):

    class Meta:
        model = Authority
        fields = [
            'user_id',
            'district',
        ]


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = [
            'user_id',
            'name',
            'district',
        ]

    def create(self, validateddata):
        try:
            authority = Authority.objects.get(
                district=validateddata['district'])
            return School.objects.create(authority=authority, **validateddata)
        except Authority.DoesNotExist:
            return School.objects.create(**validateddata)
        except Exception as e:
            pass


class AuthorityReportSerializer(serializers.Serializer):
    """
    Custom Serializer for authority reports.
    Required inputs as kwargs:
    * actual_report: Actual report object
    * estimate_report: Estimate report object of the actual report
    """

    def __init__(self, *args, **kwargs):
        actual_report = kwargs.pop('actual_report', None)
        estimate_report = kwargs.pop('estimate_report', None)
        super(AuthorityReportSerializer, self).__init__(*args, **kwargs)

        self._data = OrderedDict()

        if not (actual_report or estimate_report):
            raise ValidationError(
                _('Neither actual report nor estimate report is given.'))

        if actual_report and estimate_report:
            if actual_report.for_date != estimate_report.for_date:
                raise ValidationError(
                    _('The for date in the reports do not match.'))

            if actual_report.school != estimate_report.school:
                raise ValidationError(
                    _('The schools in the report do not match.'))

        if actual_report:
            self._data['actual_student_count'] = actual_report.student_count
            self._data['actual_items'] = ReportItemSerializer(
                actual_report.items, many=True).data
            self._data['school'] = SchoolSerializer(actual_report.school).data
            self._data['for_date'] = actual_report.for_date
        else:
            self._data['actual_student_count'] = 0
            self._data['actual_items'] = ReportItemSerializer(
                [], many=True).data

        if estimate_report:
            self._data['estimate_student_count'] = estimate_report.student_count
            self._data['estimate_items'] = ReportItemSerializer(
                estimate_report.items, many=True).data
        else:
            self._data['estimate_student_count'] = 0
            self._data['estimate_items'] = ReportItemSerializer(
                [], many=True).data


class DistrictSerializer(serializers.ModelSerializer):

    class Meta:
        model = District
        fields = '__all__'

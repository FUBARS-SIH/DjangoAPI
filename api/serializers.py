from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import CustomUser, Authority, School, Report, District, ReportItem
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
            'items'
        ]

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        report = Report.objects.create(**validated_data)
        for item_data in items_data:
            ReportItem.objects.create(report=report, **item_data)        
        return report

    @transaction.atomic
    def update(self, instance, validated_data):
        items_data = validated_data.pop('items')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if items_data:
            instance.items.all().delete()
            for item_data in items_data:
                ReportItem.objects.create(report=instance, **item_data)        
        instance.save()
        return instance

class FullReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

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

    def create(self, validated_data):
        try:
            authority = Authority.objects.get(district=validated_data['district'])
            return School.objects.create(authority=authority, **validated_data)
        except Authority.DoesNotExist:
            return School.objects.create(**validated_data)
        except Exception as e:
            pass

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'
        
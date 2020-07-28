from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import CustomUser, Authority, School, Report, District

class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = [
            'id', 
            'username',
            'email',
            'password',
            'is_authority',
        ]

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            'id',
            'reported_student_count',
            'reported_menu',
            'reported_for_date',
        ]

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
        
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import CustomUser, Authority, School, Report

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
            'reported_student_count',
            'reported_menu',
            'reported_for_date',
            'reported_on_datetime',
            'school',
        ]

class AuthoritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Authority
        fields = [
            'district',
        ]

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            'school_name',
            'authority',
        ]
from rest_framework.decorators import api_view
from django.http import JsonResponse

from rest_framework.permissions import BasePermission, IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.response import Response
from rest_framework import generics
from .permissions import IsOwnerOrReadOnly
from .serializers import ReportSerializer, AuthoritySerializer, SchoolSerializer
from .models import Report, School, Authority

from rest_framework import status
import json
from django.core.exceptions import ObjectDoesNotExist

@api_view(["GET"])
def get_reports(request):
    school_id = request.school.id
    reports = Report.objects.filter(School.objects.get(id=school_id))
    #reports = Report.objects
    serializer = ReportSerializer(reports, many=True)
    return JsonResponse({'reports': serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(["POST"])
def add_report(request):
    payload = json.loads(request.body)
    try:
        school = School.objects.get(id=payload["school_id"])
        report = Report.objects.create(
            reported_student_count=payload["student_count"],
            reported_menu=payload["menu"],
            reported_for_date=payload["for_date"],
            school=school
        )
        serializer = ReportSerializer(report)
        return JsonResponse({'report': serializer.data}, safe=False, status=status.HTTP_201_CREATED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(["PUT"])
def update_report(request, report_id):
    payload = json.loads(request.body)
    try:
        report_item = Report.objects.filter(id=report_id)
        report_item.update(**payload)
        serializer = ReportSerializer(report_item)
        return JsonResponse({'report': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AuthorityEnroll(generics.CreateAPIView):
    queryset = Authority.objects.all()
    serializer_class = AuthoritySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        user.is_authority = True
        user.save()
        return serializer.save(user=user)

class SchoolEnroll(generics.CreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class AuthorityRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = Authority.objects.all()
    serializer_class = AuthoritySerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class SchoolRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class ReportCreate(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user_id = self.request.id
        school = School.objects.filter(id = user_id) #should retive by id ther might be users with similar name
        return serializer.save(school=school)

class ReportRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
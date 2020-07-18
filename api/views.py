from rest_framework.decorators import api_view
from django.http import JsonResponse

from .serializers import ReportSerializer
from rest_framework import status
from .models import Report
import json
from django.core.exceptions import ObjectDoesNotExist

@api_view(["GET"])

def get_reports(request):
    school = request.school.id
    reports = Report.objects.filter(added_by=school)
    #reports = Report.objects
    serializer = ReportSerializer(reports, many=True)
    return JsonResponse({'reports': serializer.data}, safe=False, status=status.HTTP_200_OK)

@api_view(["POST"])

def add_report(request):
    payload = json.loads(request.body)
    try:
        school = School.objects.get(id=payload["school"])
        report = Report.objects.create(
            reported_student_count=payload["student_count"],
            reported_menu=payload["menu"],
            reported_for_date=payload["for_date"],
            reported_on_datetime=payload["on_datetime"],
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
    school = request.school.id
    payload = json.loads(request.body)
    try:
        report_item = Report.objects.filter(added_by=school, id=report_id)
        # returns 1 or 0
        report_item.update(**payload)
        report = Report.objects.get(id=report_id)
        serializer = ReportSerializer(report)
        return JsonResponse({'report': serializer.data}, safe=False, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Something terrible went wrong'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

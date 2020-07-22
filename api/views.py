from rest_framework.permissions import BasePermission, IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.http import Http404
from .permissions import IsOwnerOrReadOnly, IsSchoolOwner, IsOwner
from .serializers import ReportSerializer, AuthoritySerializer, SchoolSerializer, FullReportSerializer
from .models import Report, School, Authority

class MeRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """
    RetrieveUpdateAPIView for read and update of objects with 
    logged in user.
    """

    def get_object(self):
        """
        Returns the object of the current logged in user.
        """
        queryset = self.filter_queryset(self.get_queryset())
        try:
            obj = get_object_or_404(queryset, user=self.request.user)
            self.check_object_permissions(self.request, obj)
            return obj
        except (TypeError, ValueError, ValidationError):
            raise Http404

class AuthorityEnroll(generics.CreateAPIView):
    queryset = Authority.objects.all()
    serializer_class = AuthoritySerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        user.is_authority = True
        user.save()
        return serializer.save(user=user)

class AuthorityMeRetrieveUpdate(MeRetrieveUpdate):
    """
    Retrieve or update the current logged in authority details.
    """
    queryset = Authority.objects.all()
    serializer_class = AuthoritySerializer
    permission_classes = [IsAuthenticated, IsOwner]

class AuthorityReportList(generics.ListAPIView):
    """
    Lists all the reports created by schools under the 
    currently logged in authority.
    """
    queryset = Report.objects.all()
    serializer_class = FullReportSerializer
    permission_classes = [IsAuthenticated, IsSchoolOwner]

    def list(self, request):
        queryset = self.get_queryset()
        authority = Authority.objects.get(user=request.user)
        schools = authority.school_set.all()
        serializer = FullReportSerializer(queryset.filter(school__in=schools), many=True)
        return Response(serializer.data)


class SchoolEnroll(generics.CreateAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class SchoolMeRetrieveUpdate(MeRetrieveUpdate):
    """
    Retrieve or update the current logged in school details.
    """
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
class SchoolReportListCreate(generics.ListCreateAPIView):
    """
    Creates new reports by school.
    Lists all the reports created by a school.
    Request has to be initiated by the owner school.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated, IsSchoolOwner]

    def list(self, request):
        queryset = self.get_queryset()
        serializer = UserSerializer(queryset.filter(school__user=request.user), many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = self.request.user
        school = School.objects.get(user=user)
        return serializer.save(school=school)

class SchoolReportRetrieveUpdate(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update reports created by currently
    logged in school.
    """
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated, IsSchoolOwner]

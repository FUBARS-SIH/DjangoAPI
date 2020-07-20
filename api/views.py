from rest_framework.permissions import BasePermission, IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.response import Response
from rest_framework import generics
from .permissions import IsOwnerOrReadOnly, IsSchoolOwner
from .serializers import ReportSerializer, AuthoritySerializer, SchoolSerializer
from .models import Report, School, Authority

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
    permission_classes = [IsAuthenticated, IsSchoolOwner]

    def perform_create(self, serializer):
        user = self.request.user
        school = School.objects.get(user=user)
        return serializer.save(school=school)

class ReportRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
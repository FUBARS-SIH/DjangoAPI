from django.urls import include, path
from . import views

urlpatterns = [
  path('authority/', views.AuthorityEnroll.as_view()),
  path('authority/me/', views.AuthorityMeRetrieveUpdate.as_view()),
  path('authority/me/report/', views.AuthorityReportList.as_view()),
  path('school/', views.SchoolEnroll.as_view()),
  path('school/me/', views.SchoolMeRetrieveUpdate.as_view()),
  path('school/me/report/', views.SchoolReportListCreate.as_view()),
  path('school/me/report/<int:pk>', views.SchoolReportRetrieveUpdate.as_view()),
]
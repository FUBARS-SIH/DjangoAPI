from django.urls import include, path
from . import views

urlpatterns = [
  path('authority/', views.AuthorityEnroll.as_view(), name='authority_enroll'),
  path('authority/me/', views.AuthorityMeRetrieveUpdate.as_view(), name='authority_me_retrieve_update'),
  path('authority/me/report/', views.AuthorityReportList.as_view(), name='authority_report_list'),
  path('school/', views.SchoolEnroll.as_view(), name='school_enroll'),
  path('school/me/', views.SchoolMeRetrieveUpdate.as_view(), name='school_me_retrieve_update'),
  path('school/me/report/', views.SchoolReportListCreate.as_view(), name='school_report_list_create'),
  path('school/me/report/<int:pk>', views.SchoolReportRetrieveUpdate.as_view(), name='school_report_retrieve_update'),
]
from django.urls import include, path
from . import views

urlpatterns = [
  path('authorities/', views.AuthorityEnroll.as_view(), name='authority_enroll'),
  path('authorities/me/', views.AuthorityMeRetrieveUpdate.as_view(), name='authority_me_retrieve_update'),
  path('authorities/me/report/', views.AuthorityReportList.as_view(), name='authority_report_list'),
  path('schools/', views.SchoolEnroll.as_view(), name='school_enroll'),
  path('schools/me/', views.SchoolMeRetrieveUpdate.as_view(), name='school_me_retrieve_update'),
  path('schools/me/report/', views.SchoolReportListCreate.as_view(), name='school_report_list_create'),
  path('schools/me/report/<int:pk>', views.SchoolReportRetrieveUpdate.as_view(), name='school_report_retrieve_update'),
  path('districts/', views.DistrictList.as_view(), name='district_list'),
]
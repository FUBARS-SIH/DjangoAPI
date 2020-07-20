from django.urls import include, path
from . import views

urlpatterns = [
  path('authority/', views.AuthorityEnroll.as_view()),
  path('authority/<int:pk>', views.AuthorityRetrieveUpdate.as_view()),
  path('school/', views.SchoolEnroll.as_view()),
  path('school/<int:pk>', views.SchoolRetrieveUpdate.as_view()),
  path('report/', views.ReportCreate.as_view()),
  path('report/<int:pk>', views.ReportRetrieveUpdate.as_view()),
]
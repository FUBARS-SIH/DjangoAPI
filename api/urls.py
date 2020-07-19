from django.urls import include, path
from . import views

urlpatterns = [
  path('getreports', views.get_reports),
  path('addreport', views.add_report),
  path('updatebook/<int:book_id>', views.update_book),
]
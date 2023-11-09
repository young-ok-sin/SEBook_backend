from django.urls import path
from .views import CreateBookReport,DeleteBookReport

urlpatterns = [
    path('bookReportCreate', CreateBookReport.as_view(), name='bookReportCreate'),
    path('DeleteBookReport', DeleteBookReport.as_view(), name='bookReportdelete'),
]
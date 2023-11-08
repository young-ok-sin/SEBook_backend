from django.urls import path
from .views import CreateBookReport

urlpatterns = [
    path('bookReportCreate', CreateBookReport.as_view(), name='bookReportCreate'),
]
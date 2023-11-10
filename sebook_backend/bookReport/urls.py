from django.urls import path
from .views import CreateBookReport,DeleteBookReport,UserSavedBookReports,UserWriteBookReports

urlpatterns = [
    path('bookReportCreate', CreateBookReport.as_view(), name='bookReportCreate'),
    path('DeleteBookReport', DeleteBookReport.as_view(), name='bookReportdelete'),
    path('bookReportReadLike', UserSavedBookReports.as_view(), name='bookReportRead'),
        path('bookReportReadMy', UserWriteBookReports.as_view(), name='bookReportRead'),
]
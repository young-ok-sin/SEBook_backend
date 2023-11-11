from django.urls import path
from .views import CreateBookReport,DeleteBookReport,UserSavedBookReports,UserWriteBookReports,LikeBookReportView,ReadAllBookReport

urlpatterns = [
    path('bookReportCreate', CreateBookReport.as_view(), name='bookReportCreate'),
    path('bookReportDelete', DeleteBookReport.as_view(), name='bookReportdelete'),
    path('bookReportReadLike', UserSavedBookReports.as_view(), name='bookReportRead'),
    path('bookReportReadMy', UserWriteBookReports.as_view(), name='myBookReportRead'),
    path('bookReportLike', LikeBookReportView.as_view(), name='myBookReportRead'),
    path('bookReportReadAll', ReadAllBookReport.as_view(), name='myBookReportRead'),
]
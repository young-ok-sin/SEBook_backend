from django.urls import path
from .views import CreateBookReport,DeleteBookReport,UserSavedBookReports,UserWriteBookReports,LikeBookReportView,ReadAllBookReport,UpdateBookReport,SearchBookReportByTitle,TopRatedBookReports,SearchBookReportByAuthor

urlpatterns = [
    path('bookReportCreate', CreateBookReport.as_view(), name='bookReportCreate'),
    path('bookReportDelete', DeleteBookReport.as_view(), name='bookReportdelete'),
    path('bookReportReadLike', UserSavedBookReports.as_view(), name='bookReportReadLike'),
    path('bookReportReadMy', UserWriteBookReports.as_view(), name='bookReportReadMy'),
    path('bookReportLike', LikeBookReportView.as_view(), name='bookReportLike'),
    path('bookReportReadAll', ReadAllBookReport.as_view(), name='bookReportReadAll'),
    path('bookReportUpdate', UpdateBookReport.as_view(), name='bookReportUpdate'),
    path('bookReportSearch', SearchBookReportByTitle.as_view(), name='bookReportSearch'),
    path('bookReportReadTop5', TopRatedBookReports.as_view(), name='TopRatedBookReports'),
    path('bookReportSearchByAuthor', SearchBookReportByAuthor.as_view(), name='bookReportSearchByAuthor'),

]
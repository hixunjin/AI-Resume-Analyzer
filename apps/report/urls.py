# backend/apps/report/urls.py
from django.urls import path
from .views import ReportListView, ReportDetailView,statistics_view,download_report

urlpatterns = [
    path('', ReportListView.as_view(), name='report-list'),
    path('<int:pk>/', ReportDetailView.as_view(), name='report-detail'),
    path('stats/', statistics_view, name='report-stats'),


    #下载
    path('download_report/<int:resume_id>/', download_report, name='download_report'),
]

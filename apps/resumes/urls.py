from django.urls import path
from . import views

urlpatterns = [

    #上传接口
    path('upload/', views.upload_resume),
    path('list/', views.list_resumes),
    path('download/<int:resume_id>/', views.download_resume, name='resume_download'),
]

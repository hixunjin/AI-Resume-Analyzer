from django.contrib import admin
from django.urls import path, include,re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

#接口文档描述信息
schema_view = get_schema_view(
    openapi.Info(
        title="AI Resume Analyzer API",
        default_version='v1',
        description="接口文档（支持在线调试）",
        contact=openapi.Contact(email="you@example.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/resumes/', include('apps.resumes.urls')),
    path('api/reports/', include('apps.report.urls')),


    # Swagger & Redoc 文档
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

from django.conf import settings
from django.conf.urls.static import static

# 媒体文件访问（开发阶段）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
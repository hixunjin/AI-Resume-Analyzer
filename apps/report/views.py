from django.shortcuts import render

from rest_framework import generics
from .models import Report
from .serializers import ReportSerializer
from django.views.decorators.csrf import csrf_exempt


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.report.models import Report
from apps.report.serializers import ReportSerializer

#这个模块主要是对数据库中的报告数据进行查看，分为报告列表和详细的报告数据


#获取所有报告
class ReportListView(generics.ListAPIView):
    queryset = Report.objects.all().order_by('-created_at')
    serializer_class = ReportSerializer



# 获取单个简历的报告
class ReportDetailView(generics.RetrieveAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer



from django.db.models import Count, Avg
from django.db.models.functions import TruncDate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Report


#统计函数

@api_view(['GET'])
@permission_classes([IsAdminUser])
@csrf_exempt
def statistics_view(request):
    """
    管理员统计接口：
    - 每日调用量
    - 平均匹配度趋势
    """
    # 按日期聚合统计
    daily_stats = (
        Report.objects
        .annotate(date=TruncDate("created_at"))
        .values("date")
        .annotate(
            total_calls=Count("id"),
            avg_score=Avg("score"),
        )
        .order_by("date")
    )

    # 格式化输出
    data = {
        "dates": [item["date"].strftime("%Y-%m-%d") for item in daily_stats],
        "calls": [item["total_calls"] for item in daily_stats],
        "avg_scores": [round(item["avg_score"] or 0, 2) for item in daily_stats],
    }

    return Response(data)





import os
from io import BytesIO
from django.http import FileResponse, Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Report
from apps.resumes.models import Resume
from django.conf import settings
from rest_framework.renderers import BaseRenderer
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BaseRenderer
from django.http import FileResponse, Http404
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Report


from io import BytesIO
from django.http import FileResponse, Http404
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BaseRenderer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from .models import Report


from io import BytesIO
from django.http import FileResponse, Http404
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import BaseRenderer
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from .models import Report
import os


# PDF 渲染器（让 DRF 返回 PDF 格式）
class PDFRenderer(BaseRenderer):
    media_type = 'application/pdf'
    format = 'pdf'
    charset = None
    render_style = 'binary'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@renderer_classes([PDFRenderer])
def download_report(request, resume_id):
    """
    下载指定 resume_id 的 AI 分析报告（支持中文 PDF）
    """
    try:
        report = Report.objects.get(resume_id=resume_id)
    except Report.DoesNotExist:
        raise Http404("报告不存在")

    # ✅ 注册本地中文字体
    font_path = r"C:\Windows\Fonts\msyh.ttc"  # 微软雅黑字体路径
    if not os.path.exists(font_path):
        raise FileNotFoundError("字体文件未找到，请检查路径！")

    pdfmetrics.registerFont(TTFont('msyh', font_path))

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("msyh", 12)

    # 开始绘制 PDF 内容
    y = 800
    line_height = 22

    def draw_line(text):
        """自动换行绘制"""
        nonlocal y
        max_width = 500
        lines = []
        while len(text) > 0:
            width = p.stringWidth(text, "msyh", 12)
            if width <= max_width:
                lines.append(text)
                break
            for i in range(len(text), 0, -1):
                if p.stringWidth(text[:i], "msyh", 12) <= max_width:
                    lines.append(text[:i])
                    text = text[i:]
                    break
        for line in lines:
            p.drawString(72, y, line)
            y -= line_height

    draw_line(f"AI 简历分析报告 - {report.resume.file.name}")
    draw_line(f"匹配度评分：{report.score}")
    draw_line("【简历摘要】")
    draw_line(report.summary or "无摘要")
    draw_line("【优化建议】")
    draw_line(report.suggestions or "无建议")

    p.showPage()
    p.save()
    buffer.seek(0)

    filename = f"AI分析报告_{resume_id}.pdf"
    response = FileResponse(buffer, as_attachment=True, filename=filename)
    response['Content-Type'] = 'application/pdf'
    return response
